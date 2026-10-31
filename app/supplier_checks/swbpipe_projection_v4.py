"""V4 offline receiving specimen. No host IO, native applier or publication authority."""
import copy
import json
from swbpipe_projection import decode, expand, validate, validate_assumptions


def response(catalog, tool, result):
    """V4 fixture wire: preserve Unicode text and escape lone surrogates.

    Numeric serialization remains Python's fixture representation; this is not
    an implementation of the host's negative-zero/numeric canonicalizer.
    """
    validate(result, expand(catalog, tool['outputSchema']))
    if result['status'] in ('ok', 'completed', 'pending_review', 'applied') and result['data'] is None:
        raise ValueError('missing outcome data')
    data = result['data']
    if data and 'values' in data:
        for row in data['values']:
            if row['availability'] != 'available' and (row['value'] is not None or row['exactDecimal'] is not None or not row['reason']):
                raise ValueError('withheld value')
    text = json.dumps(result, ensure_ascii=False, allow_nan=False, separators=(',', ':'))
    text = text.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')
    text = ''.join('\\u%04x' % ord(c) if 0xD800 <= ord(c) <= 0xDFFF else c for c in text)
    if len(text.encode('utf-8')) > catalog['limits']['resultBytes']:
        raise ValueError('result byte admission')
    return {'contentItems': [{'type': 'inputText', 'text': text}],
            'success': result['status'] != 'execution_error'}


def admit_operations(catalog, operations):
    rows = catalog.get('admittedOperations')
    if not isinstance(rows, list) or not rows:
        raise ValueError('missing admitted operation table')
    allowed = set()
    for row in rows:
        if set(row) != {'operationKind', 'objectType', 'changeKind', 'fieldPaths'}:
            raise ValueError('invalid admitted operation row')
        for path in row['fieldPaths']:
            key = (row['operationKind'], row['objectType'], row['changeKind'], path)
            if key in allowed:
                raise ValueError('duplicate admitted operation tuple')
            allowed.add(key)
    for op in operations:
        key = (op['operation_kind'], op['target']['object_type'],
               op['change']['change_kind'], op['change']['field_path'])
        if key not in allowed:
            raise ValueError('operation tuple not admitted')


def page_context(tool, args):
    return {'tool': tool, 'workspaceHandle': args['workspaceHandle'],
            'basis': copy.deepcopy(args['basis']), 'runHandle': args.get('runHandle'),
            'family': args.get('family'), 'filter': copy.deepcopy(args.get('filter'))}


def check_cursor(tool, args, retained_cursor):
    cursor = args.get('page', {}).get('cursor')
    if cursor is None:
        return
    if not retained_cursor or retained_cursor.get('handle') != cursor:
        raise ValueError('missing or mismatched retained cursor')
    if retained_cursor.get('context') != page_context(tool, args):
        raise ValueError('cursor context mismatch')
    offset = retained_cursor.get('nextOffset')
    if type(offset) is not int or offset < 0:
        raise ValueError('cursor next offset invalid')


def js_text_bytes(text):
    # TextEncoder replaces lone UTF-16 surrogates with U+FFFD.
    return text.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'replace').encode('utf-8')


def js_string(text):
    # The entry grammar contains strings only. JSON.stringify escapes lone
    # surrogates, controls, quotes and backslashes; it emits other Unicode raw.
    normalized = text.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')
    quoted = json.dumps(normalized, ensure_ascii=False, separators=(',', ':'))
    return ''.join('\\u%04x' % ord(c) if 0xD800 <= ord(c) <= 0xDFFF else c for c in quoted)


def entry_bytes(row):
    # Producer creates keys in this order. before's contract keys are nonnumeric;
    # order affects bytes but not the byte count. No numeric values are serialized.
    before = '{' + ','.join(js_string(k) + ':' + js_string(v) for k, v in row['before'].items()) + '}'
    return ('{"id":' + js_string(row['id']) + ',"recordText":' + js_string(row['recordText'])
            + ',"before":' + before + '}').encode('utf-8')


def check_records(args, result):
    data = result['data']
    if data is None:
        return
    if data['family'] != args['family']:
        raise ValueError('record family mismatch')
    if len(data['records']) > args['page']['limit']:
        raise ValueError('record page exceeds requested rows')
    total = 0
    for row in data['records']:
        if len(row['id'].encode('utf-16-le', 'surrogatepass')) // 2 > 160:
            raise ValueError('record id UTF16 length')
        for text in [row['recordText'], *row['before'].values()]:
            if len(js_text_bytes(text)) > 16384:
                raise ValueError('record text UTF8 byte bound')
        total += len(entry_bytes(row))
        if total > 49152:
            raise ValueError('serialized record page byte bound')


def expected_record_page(entries, offset, limit):
    """Fixture-only receiving expectation over already canonical host entries.

    No raw model parsing or applier formatting. A bad encountered record fails
    the entire call, including records that preceded it. A fitting next entry
    beyond the aggregate budget belongs to the next page.
    """
    selected = []; total = 0; end = offset
    while end < len(entries) and len(selected) < limit:
        row = entries[end]
        if (not isinstance(row.get('id'), str) or not row['id']
                or len(row['id'].encode('utf-16-le', 'surrogatepass')) // 2 > 160
                or any(len(js_text_bytes(t)) > 16384 for t in [row['recordText'], *row['before'].values()])):
            return 'unavailable', [], None
        size = len(entry_bytes(row))
        if size > 49152:
            return 'unavailable', [], None
        if total + size > 49152:
            break
        selected.append(copy.deepcopy(row)); total += size; end += 1
    return 'ok', selected, end if end < len(entries) else None


def check_records_observation(args, result, retained_page, retained_cursor=None):
    """Join a result to independently supplied invented host page evidence."""
    check_cursor('swbpipe_read_records', args, retained_cursor)
    expected_offset = 0 if args['page']['cursor'] is None else retained_cursor['nextOffset']
    if retained_page['offset'] != expected_offset:
        raise ValueError('retained page offset mismatch')
    if retained_page['context'] != page_context('swbpipe_read_records', args):
        raise ValueError('retained record page context mismatch')
    status, rows, next_offset = expected_record_page(retained_page['entries'], retained_page['offset'], args['page']['limit'])
    current = retained_page.get('current_basis', args['basis'])
    # Entry drift precedes record validation; drift during reading follows it.
    # Without timing evidence, an invalid encountered record may legitimately
    # yield unavailable or the entry check's stale_basis, never a partial pass.
    if current != args['basis'] and (status == 'ok' or result['status'] == 'stale_basis'):
        if result['status'] != 'stale_basis' or result['data'] is not None or result['basis'] != args['basis']:
            raise ValueError('stale record page outcome mismatch')
        return
    # The actual serialized result is supplied separately, never synthesized by
    # Python number formatting. Producer small() limits its complete UTF8 bytes.
    if status == 'ok':
        candidate = decode(retained_page['serialized_result'], 131072)
        if (candidate.get('status') != 'ok' or candidate.get('basis') != args['basis']
                or candidate.get('data', {}).get('family') != args['family']
                or candidate.get('data', {}).get('records') != rows):
            raise ValueError('serialized page evidence mismatch')
        if len(retained_page['serialized_result']) > 65536:
            status = 'execution_error'
    if result['status'] != status:
        raise ValueError('record page outcome mismatch')
    if status != 'ok':
        if result['data'] is not None:
            raise ValueError('failed record call cannot return a partial page')
        return
    if result['data']['records'] != rows:
        raise ValueError('record page truncated, skipped or substituted')
    if candidate != result:
        raise ValueError('serialized page evidence mismatch')
    if (result['data']['nextCursor'] is None) != (next_offset is None):
        raise ValueError('record page continuation mismatch')


def check_before(operation, basis, retained):
    """Compare opaque host-supplied before text; never derive applier semantics."""
    if retained is None or retained.get('basis') != basis or retained.get('target') != operation['target']:
        raise ValueError('missing retained target before text')
    key = 'delete' if operation['operation_kind'] == 'delete' else operation['change']['field_path']
    expected = retained.get('before', {}).get(key)
    if expected is None:
        raise ValueError('before text unavailable')
    if operation['change']['before'] != expected:
        raise ValueError('before text mismatch')


class Pending:
    """One invented pending call. Production must also own queues, cursors and budgets."""
    def __init__(self, catalog, binding, args_raw, current_basis, current_units=None, retained_record=None, retained_cursor=None, retained_before=None):
        catalog = copy.deepcopy(catalog)
        self.catalog = catalog
        if catalog["catalogVersion"] != "swbpipe-catalog/4":
            raise ValueError("unsupported catalog version")
        self.retained_policy = catalog["catalogVersion"] in ("swbpipe-catalog/4",)
        historical = self.retained_policy and binding.get("tool") in (
            "swbpipe_observe_proposal", "swbpipe_read_results")
        captured_basis = current_basis
        if historical:
            if retained_record is None:
                raise ValueError("missing retained record")
            captured_basis = retained_record["basis"]
            validate(captured_basis, expand(catalog, catalog["definitions"]["basis"]))
            for key in ("workspaceHandle", "applicationGeneration"):
                if captured_basis[key] != current_basis[key]:
                    raise ValueError("retained session mismatch")
        self.binding = copy.deepcopy(binding)
        validate(current_basis, expand(catalog, catalog["definitions"]["basis"]))
        if set(binding) != set(catalog["hostPolicy"]["binding"]):
            raise ValueError("binding fields")
        for key in ("workspaceHandle", "applicationGeneration", "modelRevision"):
            if type(binding[key]) is not type(captured_basis[key]) or binding[key] != captured_basis[key]:
                raise ValueError("binding basis")
        for key in ("requestRef", "threadId", "turnId", "callId", "tool"):
            if not isinstance(binding[key], str) or not binding[key]:
                raise ValueError("binding identity")
        if type(binding["rpcId"]) not in (str, int):
            raise ValueError("RPC identity")
        self.tool = next(t for t in catalog["tools"] if t["name"] == binding["tool"])
        self.args = decode(args_raw, catalog["limits"]["argumentBytes"])
        validate(self.args, expand(catalog, self.tool["inputSchema"]))
        check_cursor(binding['tool'], self.args, retained_cursor)
        self.basis = copy.deepcopy(captured_basis)
        if historical:
            handle_key = "proposalHandle" if binding["tool"] == "swbpipe_observe_proposal" else "runHandle"
            if self.args[handle_key] != retained_record["handle"]:
                raise ValueError("retained handle mismatch")
        if self.args.get("workspaceHandle", current_basis["workspaceHandle"]) != current_basis["workspaceHandle"]:
            raise ValueError("workspace")
        if self.args.get("basis", captured_basis) != captured_basis:
            raise ValueError("stale basis")
        if "claimedModelHash" in self.args and (self.args["claimedModelHash"] != current_basis["modelHash"]):
            raise ValueError("claimed hash")
        if len(self.args.get("operations", [])) > catalog["limits"]["proposalOperations"]:
            raise ValueError("configured batch limit")
        if self.retained_policy and "operations" in self.args:
            validate_assumptions(self.args["operations"], self.args["assumptions"])
        if "operations" in self.args:
            admit_operations(catalog, self.args["operations"])
            for intent in self.args["operations"]:
                needs_before = (intent['operation_kind'] == 'delete'
                                or intent['change']['field_path'] in (
                                    'configuration', 'objective_connector.hardware',
                                    'objective_connector.pressure_model'))
                if needs_before:
                    check_before(intent, self.basis, (retained_before or {}).get(intent['operation_id']))
                # Preserve the original coordinate-unit guard. V4's flat intent
                # subschemas admit other dimensions; their native payload/unit
                # semantics stay with SWBPIPE's applier. Description text is not
                # executable validation or a source of new permissions.
                coordinate = (intent["target"]["object_type"] == "Node"
                              and intent["change"]["change_kind"] == "set_field")
                if coordinate:
                    if not current_units or not current_units.get("length"):
                        raise ValueError("units unavailable")
                    if intent["change"]["unit"] != current_units["length"]:
                        raise ValueError("document unit mismatch")
        self.completed = False

    def complete(self, binding, result, current_basis, retained_record=None, session_attached=True):
        if not session_attached:
            raise ValueError("detached session")
        if self.completed:
            raise ValueError("duplicate")
        if binding != self.binding:
            raise ValueError("correspondence")
        for key in ("workspaceHandle", "applicationGeneration"):
            if current_basis[key] != self.basis[key] or result["basis"][key] != self.basis[key]:
                raise ValueError("session changed")
        historical_completion = self.retained_policy and self.binding["tool"] not in (
            "swbpipe_read_model_summary", "swbpipe_read_nodes", "swbpipe_read_records")
        for key in ("modelRevision", "modelHash"):
            if result["basis"][key] != self.basis[key]:
                raise ValueError("result rebased")
            stale_records = (self.binding["tool"] == "swbpipe_read_records"
                             and result["status"] == "stale_basis" and result["data"] is None)
            if not historical_completion and current_basis[key] != self.basis[key] and not stale_records:
                raise ValueError("basis changed")
        if historical_completion and result["data"] is not None:
            # Fixture-only host-owned record, supplied separately from the untrusted completion.
            # This is NOT an extra field in the webview completion wire.
            if retained_record is None or retained_record["binding"] != self.binding:
                raise ValueError("missing or mismatched retained completion")
            if retained_record["basis"] != self.basis or retained_record["result"] != result:
                raise ValueError("forged retained outcome")
        # Validate shape before examining bounded record fields.
        validate(result, expand(self.catalog, self.tool['outputSchema']))
        if self.binding['tool'] == 'swbpipe_read_records':
            check_records(self.args, result)
        wire = response(self.catalog, self.tool, result)
        self.completed = True
        return {"id": self.binding["rpcId"], "result": wire}
