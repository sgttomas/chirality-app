#!/usr/bin/env python3
"""Design checker: a design record against its pattern catalogue and specification.

Part of the data-app-spec workflow; requires PyYAML and jsonschema. It checks that a design record is well formed, that its
choices are recorded as ruled by a ruling whose scope, authority and decision-record
digest agree, that the patterns it uses have their authoring questions answered or
recorded as gaps, and, when a specification is given, that every need traces to
specification elements. It reads records: it cannot establish that a person made a
ruling, and it does not establish that the design is right or adequate.

Usage:
    python3 -I check_design.py --schemas DIR --catalogue CATALOGUE.yaml DESIGN.yaml [--spec SPEC.yaml]
    python3 -I check_design.py --digest RULING_ID DESIGN.yaml

DIR holds app-design.schema.json, app-patterns.schema.json and app-spec.schema.json.
`--digest` prints the digest of what a ruling's scope covers, for the design decision
record (resources/contract.md).
Exit status: 0 when every document parses and validates and no rule reports an error;
1 otherwise; 2 on bad invocation. Warnings and verdicts do not change the exit status.
The rules are listed in formats/DESIGN_ONTOLOGY.md §6. From the package folder, DIR is
`formats` and CATALOGUE is `formats/patterns.yaml`.
"""
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

import jsonschema
import yaml


def _load_check_spec():
    path = Path(__file__).with_name("check_spec.py")
    module_spec = importlib.util.spec_from_file_location("check_spec", path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


check_spec = _load_check_spec()

VIEW_LIKE = {"View", "Metric", "Export", "TextBlock", "Caveat", "Message"}
TRACE_CLASSES = {
    ("Subject", "represented_by"): {"EntityType"},
    ("DataHolding", "realized_by"): {"DataNode"},
    ("KnowledgeNeed", "satisfied_by"): {"Criterion", "Method", "ParameterTable", "Definition", "ClassificationScheme",
                                        "KnowledgePackRef", "Assumption", "Caveat", "DataNode"},
    ("NonUse", "disclosed_by"): {"TextBlock", "TextView", "Caveat", "DocumentView"},
    ("Concern", "measured_by"): {"Metric", "Objective"},
}
FACETS = {"goals": "goal", "searches": "search", "queries": "query", "targets": "target",
          "cardinalities": "cardinality", "templates": "template", "decision_stages": "decision_stage",
          "local_tasks": "local_task"}
SPECIALIST_AUTHORITIES = ("domain_expert", "accountable_professional")
DIGEST_LINE = re.compile(r"^Digest ([a-z][a-z0-9_]*): ([a-f0-9]{64})\s*$", re.M)
RULINGS_LINE = re.compile(r"^Rulings (made|returned):(.*)$", re.M)
IDENTIFIER = re.compile(r"[a-z][a-z0-9_]*")


def task_text(task):
    """Compact form of a need's task facets for reports."""
    parts = [task.get(f) for f in ("query", "target", "cardinality")]
    extra = [f"{k}={task[k]}" for k in ("search", "goal", "template", "decision_stage", "local_task") if task.get(k)]
    return "/".join(p or "?" for p in parts) + (f" ({', '.join(extra)})" if extra else "")


def subspace_matches(task, subspace):
    """A task is in a subspace when every facet the subspace lists takes one of the listed values."""
    return all(task.get(facet) in subspace[plural] for plural, facet in FACETS.items() if subspace.get(plural))


class DesignWalker(check_spec.Walker):
    """Walker that also collects cross-document references (SpecRef, PatternRef)."""

    def __init__(self, schema):
        super().__init__(schema)
        self.spec_refs = []      # (path, value, owner_class, slot)
        self.pattern_refs = []   # (path, value, owner_class, slot)

    def walk_value(self, value, schema, path, owner, slot):
        kind = schema.get("x-appspec-type") if schema else None
        if kind == "SpecRef" and isinstance(value, str):
            self.spec_refs.append((path, value, owner, slot))
            return
        if kind == "PatternRef" and isinstance(value, str):
            self.pattern_refs.append((path, value, owner, slot))
            return
        super().walk_value(value, schema, path, owner, slot)


def read_yaml(path):
    return yaml.load(Path(path).read_text(encoding="utf-8"), Loader=check_spec.Yaml12Loader)


def load_document(path, schema, root, label, report):
    """Parse and structurally validate one document. Returns the document or None."""
    try:
        document = read_yaml(path)
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        report.append(f"- {label} `{path}`: PARSE FAIL - {type(exc).__name__}: {' '.join(str(exc).split())[:300]}")
        return None
    if not isinstance(document, dict):
        report.append(f"- {label} `{path}`: PARSE FAIL - the document is not a mapping")
        return None
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    errors = sorted(validator.iter_errors(document), key=lambda e: list(e.absolute_path))
    if errors:
        report.append(f"- {label} `{path}`: SCHEMA FAIL ({len(errors)} errors)")
        for err in errors[:40]:
            report.append(f"  - `{'/'.join(str(p) for p in err.absolute_path)}`: {err.message[:240]}")
        return None
    report.append(f"- {label} `{path}`: SCHEMA PASS ({root})")
    return document


def walk(schema, document, root, walker_class=check_spec.Walker):
    walker = walker_class(schema)
    walker.walk_object(document, root, "$")
    return walker


def reference_findings(walker, label):
    findings = []
    for ident, first, second in walker.dupes:
        findings.append(f"ERROR D-ID {label}: duplicate id `{ident}` at {first} and {second}")
    for path, expected, value, _owner, _slot in walker.refs:
        if value not in walker.ids:
            findings.append(f"ERROR D-REF {label}: {path} -> `{value}` does not resolve (expected {expected})")
        elif expected not in walker.parents(walker.ids[value][0]):
            findings.append(f"ERROR D-REF {label}: {path} -> `{value}` is {walker.ids[value][0]}, expected {expected}")
    return findings


def objects(walker, cls):
    return [obj for _path, obj in walker.objects.get(cls, [])]


def check_catalogue(catalogue, walker, spec_defs):
    findings = reference_findings(walker, "catalogue")
    for pattern in catalogue.get("patterns", []) or []:
        keys = [q["key"] for q in pattern.get("settles", []) or []]
        for key in sorted({k for k in keys if keys.count(k) > 1}):
            findings.append(f"ERROR D-CAT pattern `{pattern['id']}` repeats authoring question `{key}`")
        for element in pattern.get("provides", []) or []:
            if element["kind"] not in spec_defs:
                findings.append(f"ERROR D-CAT pattern `{pattern['id']}` provides `{element['kind']}`, which is not an app_family class")
    return findings


# ----- rulings: what a ruling covers, and whether the record of it holds together -----

def elements_by_id(document):
    """Every mapping with an `id` in the document, first occurrence wins."""
    found, stack = {}, [document]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            if isinstance(node.get("id"), str):
                found.setdefault(node["id"], node)
            stack.extend(node.values())
        elif isinstance(node, list):
            stack.extend(node)
    return found


def resolve_scope_entry(design, by_id, entry):
    """A ruling's scope entry: an element id, a choice's settled key (`choice.key`) or a root slot."""
    head, _, rest = entry.partition(".")
    if head in by_id:
        node = by_id[head]
        if rest:
            settled = {s.get("key"): s for s in node.get("settled", []) or []}
            return settled.get(rest)
        return node
    return design.get(entry)


def ruling_digest(design, ruling):
    """SHA-256 of what a ruling's scope covers, including the gaps its covered choices cite."""
    by_id = elements_by_id(design)
    covered = [{"entry": e, "value": resolve_scope_entry(design, by_id, e)} for e in sorted(ruling.get("scope", []) or [])]
    cited = set()
    for item in covered:
        value = item["value"] if isinstance(item["value"], dict) else {}
        for settled in value.get("settled", []) or [value]:
            if isinstance(settled, dict) and settled.get("gap"):
                cited.add(settled["gap"])
    covered += [{"entry": f"gap:{g}", "value": by_id.get(g)} for g in sorted(cited)]
    text = json.dumps(covered, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def decision_record(design_path, evidence):
    """The DESIGN_DECISION.md a ruling's evidence names, if it exists."""
    for token in re.split(r"[\s,;]+", evidence or ""):
        if token.endswith("DESIGN_DECISION.md"):
            path = Path(token) if Path(token).is_absolute() else Path(design_path).parent / token
            if path.is_file():
                return path
    return None


class RulingBook:
    """Rulings as recorded, with each made ruling checked against its decision record."""

    def __init__(self, design, design_path, rulings):
        self.rulings = rulings
        self.valid = {}
        self.findings = []
        for ruling_id, ruling in rulings.items():
            if ruling.get("status") != "made":
                continue
            if not (ruling.get("decided_by") and ruling.get("evidence")):
                self.findings.append(f"ERROR D-RUL ruling `{ruling_id}` is marked made without decided_by and evidence")
                continue
            record = decision_record(design_path, ruling["evidence"])
            if record is None:
                self.findings.append(f"ERROR D-RUL2 ruling `{ruling_id}` is marked made, but its evidence names no existing DESIGN_DECISION.md")
                continue
            text = record.read_text(encoding="utf-8")
            listed = {kind: set() for kind in ("made", "returned")}
            for kind, rest in RULINGS_LINE.findall(text):
                listed[kind].update(IDENTIFIER.findall(rest))
            if ruling_id not in listed["made"] or ruling_id in listed["returned"]:
                self.findings.append(f"ERROR D-RUL4 ruling `{ruling_id}` is marked made, but {record.name} does not list it under 'Rulings made'")
                continue
            digests = dict(DIGEST_LINE.findall(text))
            if digests.get(ruling_id) != ruling_digest(design, ruling):
                self.findings.append(f"ERROR D-RUL3 ruling `{ruling_id}`: what its scope covers no longer matches the digest in {record.name} (changed after the ruling, or no digest recorded)")
                continue
            self.valid[ruling_id] = ruling

    def state(self, ruling_id, entry, authority=None):
        """Returns (state, finding). The finding is an error when the citation itself is wrong."""
        ruling = self.rulings.get(ruling_id)
        if ruling is None:
            return "invalid", None   # unresolved references are reported by D-REF
        if entry not in (ruling.get("scope") or []) and entry.split(".")[0] not in (ruling.get("scope") or []):
            return "invalid", f"ERROR D-CH4 `{entry}` cites ruling `{ruling_id}`, whose scope does not include it"
        if authority == "owner" and ruling.get("authority") == "delegated":
            return "invalid", f"ERROR D-CH7 `{entry}` is reserved to the owner but cites `{ruling_id}`, a delegated ruling"
        if authority and ruling.get("authority") != authority:
            return f"awaiting a ruling by {authority} (`{ruling_id}` is by {ruling.get('authority') or 'unstated'})", None
        if ruling_id in self.valid:
            return "recorded as ruled", None
        return f"awaiting ruling `{ruling_id}`", None


def check_design(design, walker, patterns, design_path):
    """Rules on the design record alone. Returns findings and the account of what is recorded as ruled."""
    findings = reference_findings(walker, "design")
    rulings = {r["id"]: r for r in objects(walker, "Ruling")}
    book = RulingBook(design, design_path, rulings)
    findings += book.findings
    knowledge_needs = {k["id"]: k for k in objects(walker, "KnowledgeNeed")}
    for ruling_id in list(book.valid):
        for entry in book.valid[ruling_id].get("scope", []) or []:
            knowledge = knowledge_needs.get(entry)
            if knowledge is None:
                continue
            problem = adopted_content_problem(knowledge, design_path)
            if problem:
                findings.append(f"ERROR D-RUL5 ruling `{ruling_id}` adopts knowledge need `{entry}`, but {problem}")
                book.valid.pop(ruling_id, None)
                break

    needs = {n["id"]: n for n in objects(walker, "InformationNeed")}
    decisions = {d["id"]: d for d in objects(walker, "Decision")}
    options = {o["id"]: o for o in objects(walker, "DesignOption")}
    delegations = {d["id"]: d for d in objects(walker, "Delegation")}
    alternatives = {a["id"]: a for a in objects(walker, "Alternative")}
    non_uses = {n["id"]: n for n in objects(walker, "NonUse")}
    actors = {a["id"]: a for a in objects(walker, "Actor")}
    gaps = {g["id"]: g for g in objects(walker, "Gap")}
    open_gap_targets = {a.split(".")[0] for g in gaps.values() if g.get("status") == "open" for a in g.get("affects", [])}

    asked = {actor for need in needs.values() for actor in need.get("asked_by", [])}
    for actor in objects(walker, "Actor"):
        if "user" in actor.get("roles", []) and actor["id"] not in asked:
            findings.append(f"WARN D-U1 user `{actor['id']}` asks no information need")
    ungrounded_needs = []
    for need in needs.values():
        if not (need.get("for_activities") or need.get("for_decisions")):
            findings.append(f"WARN D-N0 need `{need['id']}` serves no activity or decision")
        task = need.get("task") or {}
        if task.get("query") == "compare" and task.get("cardinality") == "single":
            findings.append(f"ERROR D-TK1 need `{need['id']}`: compare needs cardinality multiple or all")
        evaluative = task.get("goal") == "discover_confirm" or task.get("local_task") == "monitor"
        if evaluative and not need.get("interpretation"):
            findings.append(f"WARN D-IM1 need `{need['id']}` is evaluative but states no interpretation (what counts as met or missed)")
        if not need.get("basis"):
            ungrounded_needs.append(need["id"])
    if ungrounded_needs:
        findings.append(f"WARN D-GR1 needs without a basis (how each was found): {', '.join(ungrounded_needs)}")
    used_knowledge = {k for need in needs.values() for k in need.get("needs_knowledge", [])}
    for knowledge in objects(walker, "KnowledgeNeed"):
        if knowledge["id"] not in used_knowledge:
            findings.append(f"WARN D-K0 knowledge need `{knowledge['id']}` is used by no information need")

    unadopted = {}
    for decision in decisions.values():
        listed = decision.get("alternatives", [])
        if not listed:
            findings.append(f"ERROR D-D1 decision `{decision['id']}` names no alternatives")
        elif not any(alternatives.get(a, {}).get("status_quo") for a in listed):
            findings.append(f"WARN D-D1 decision `{decision['id']}` has no status-quo alternative")
        if not decision.get("concerns"):
            findings.append(f"WARN D-D1 decision `{decision['id']}` names no concerns")
        role = decision.get("app_role")
        if role in ("rank", "recommend"):
            if not decision.get("adopted_by"):
                findings.append(f"ERROR D-D2 decision `{decision['id']}`: the app {role}s alternatives but names no ruling that adopts the logic or weights")
            else:
                state, finding = book.state(decision["adopted_by"], decision["id"], decision_logic_authority(actors, decision))
                if finding:
                    findings.append(finding)
                if state != "recorded as ruled":
                    unadopted[decision["id"]] = state
                scope = rulings.get(decision["adopted_by"], {}).get("scope") or []
                rule_needs = sorted({k for n in needs.values() if decision["id"] in n.get("for_decisions", [])
                                     for k in n.get("needs_knowledge", [])
                                     if knowledge_needs.get(k, {}).get("kind") in ("decision_rule", "expert_judgment")})
                for knowledge_id in rule_needs:
                    if knowledge_id not in scope:
                        findings.append(f"ERROR D-D5 decision `{decision['id']}`: ruling `{decision['adopted_by']}` adopts its logic but does not name the knowledge need `{knowledge_id}` that holds it")
        shared = set.intersection(*[set(alternatives.get(a, {}).get("realized_by", [])) for a in listed]) if listed else set()
        if shared and role not in ("rank", "recommend"):
            findings.append(f"ERROR D-D3 decision `{decision['id']}`: every alternative is realised by the same element ({', '.join(sorted(shared))}), which proposes an alternative per subject, so app_role must be recommend (or rank), not {role}")
        disclosure = decision.get("decision_disclosure")
        if not disclosure:
            findings.append(f"ERROR D-D4 decision `{decision['id']}` names no non-use telling users that the decision is the decision maker's")
        elif non_uses.get(disclosure, {}).get("disclose") is False:
            findings.append(f"ERROR D-D4 decision `{decision['id']}`: its disclosure `{disclosure}` is marked not to be disclosed")
        elif not re.search(r"decid|decision", non_uses.get(disclosure, {}).get("statement", ""), re.I):
            findings.append(f"WARN D-D4 decision `{decision['id']}`: its disclosure `{disclosure}` does not say who decides")

    tier = design.get("tier")
    tier_state = "not proposed"
    if not tier:
        findings.append("WARN D-T0 no consequence tier is proposed")
    else:
        if not tier.get("grounds"):
            findings.append("WARN D-T0 the tier proposal cites no error consequences")
        if tier.get("ruling"):
            tier_state, finding = book.state(tier["ruling"], "tier", "owner")
            if finding:
                findings.append(finding)
        else:
            tier_state = "no ruling named"

    for path, value, _owner, _slot in walker.pattern_refs:
        if value not in patterns:
            findings.append(f"ERROR D-P0 {path} -> pattern `{value}` is not in the catalogue")
    for option in options.values():
        pattern = patterns.get(option.get("pattern"))
        if not pattern:
            continue
        for need_id in option.get("for_needs", []):
            task = needs.get(need_id, {}).get("task")
            if task and not any(subspace_matches(task, sub) for sub in pattern.get("addresses", [])):
                findings.append(f"WARN D-P1 option `{option['id']}`: pattern `{pattern['id']}` does not address need `{need_id}`'s task {task_text(task)}")

    for delegation in delegations.values():
        if "consequential" in delegation.get("covers", []):
            findings.append(f"ERROR D-DEL delegation `{delegation['id']}` covers consequential choices, which need a ruling that names them")

    covered, binding, unanswered, specialist = set(), {}, {}, {}
    counts = {"asked": 0, "answered": 0, "open_gaps": 0, "ruled_around": 0}
    ungrounded_answers = []
    for choice in objects(walker, "DesignChoice"):
        option = options.get(choice.get("selects"), {})
        covered.update(option.get("for_needs", []))
        covered.update(option.get("for_decisions", []))
        category = choice.get("category")
        if choice.get("ruling"):
            state, finding = book.state(choice["ruling"], choice["id"], "owner")
        elif choice.get("delegation"):
            delegation = delegations.get(choice["delegation"], {})
            finding = None
            if category == "consequential":
                finding, state = f"ERROR D-CH2 choice `{choice['id']}` is consequential but cites only a delegation", "invalid"
            elif category not in delegation.get("covers", []):
                finding, state = f"ERROR D-CH2 choice `{choice['id']}`: delegation `{choice['delegation']}` does not cover `{category}` choices", "invalid"
            else:
                state, finding = book.state(delegation.get("ruling"), delegation.get("id", ""), "owner")
                state = state.replace("recorded as ruled", "recorded as ruled (delegated)")
        else:
            finding, state = f"ERROR D-CH2 choice `{choice['id']}` names neither a ruling nor a delegation; an author cannot originate a choice", "invalid"
        if finding:
            findings.append(finding)
        binding[choice["id"]] = f"{category}; {state}"
        pattern = patterns.get(option.get("pattern"))
        if not pattern:
            continue
        settled = {s["key"]: s for s in choice.get("settled", []) or []}
        expected = [q["key"] for q in pattern.get("settles", []) or []]
        counts["asked"] += len(expected)
        for key in settled:
            if key not in expected:
                findings.append(f"ERROR D-CH3 choice `{choice['id']}` settles `{key}`, which pattern `{pattern['id']}` does not ask")
        defaults = {q["key"]: q.get("default_authority") for q in pattern.get("settles", []) or []}
        missing = []
        for key in expected:
            entry = settled.get(key)
            if not entry or not (entry.get("answer") or entry.get("gap")):
                missing.append(key)
                continue
            if not entry.get("answer"):
                gap = gaps.get(entry["gap"], {})
                status = gap.get("status")
                if status == "open":
                    counts["open_gaps"] += 1
                elif status == "ruled_around" and any(entry["gap"] in (r.get("scope") or []) for r in book.valid.values()):
                    counts["ruled_around"] += 1
                elif status == "ruled_around":
                    findings.append(f"WARN D-GAP1 gap `{entry['gap']}` is marked ruled around, but no made ruling names it; it counts as open")
                    counts["open_gaps"] += 1
                else:
                    findings.append(f"WARN D-GAP2 `{choice['id']}.{key}` cites gap `{entry['gap']}` as {status or 'missing'}, but has no answer; write the answer, with its basis and ruling")
                    missing.append(key)
                continue
            counts["answered"] += 1
            if not entry.get("basis"):
                ungrounded_answers.append(f"{choice['id']}.{key}")
            authority = entry.get("authority")
            if defaults.get(key) in SPECIALIST_AUTHORITIES and authority not in SPECIALIST_AUTHORITIES + ("owner",):
                findings.append(f"WARN D-CH8 `{choice['id']}.{key}`: the pattern marks this as a specialist judgment, but the answer names no authority")
            if authority in SPECIALIST_AUTHORITIES:
                specialist_state = specialist_answer_state(book, rulings, f"{choice['id']}.{key}", authority)
                if specialist_state != "recorded as ruled":
                    specialist[f"{choice['id']}.{key}"] = specialist_state
        if missing:
            unanswered[choice["id"]] = missing
    if ungrounded_answers:
        findings.append(f"WARN D-GR1 answers without a basis: {len(ungrounded_answers)} ({', '.join(ungrounded_answers[:6])}{' ...' if len(ungrounded_answers) > 6 else ''})")

    unaddressed, conditions = [], []
    for obligation in objects(walker, "Obligation"):
        if obligation.get("met_by_act"):
            conditions.append(obligation["id"])
        if not obligation.get("addressed_by") and obligation["id"] not in open_gap_targets:
            findings.append(f"WARN D-OB1 obligation `{obligation['id']}` is addressed by nothing and no open gap records it")
            unaddressed.append(obligation["id"])
    unchosen = [i for i in list(needs) + list(decisions) if i not in covered]
    return findings, {"binding": binding, "unanswered": unanswered, "unchosen": unchosen, "tier": tier_state,
                      "specialist": specialist, "unadopted": unadopted, "counts": counts,
                      "unaddressed": unaddressed, "conditions": conditions,
                      "open_gap_targets": open_gap_targets, "gaps": gaps,
                      "ruled_gaps": {g for r in book.valid.values() for g in (r.get("scope") or []) if g in gaps}}


def adopted_content_problem(knowledge, design_path):
    """Why a ruling cannot adopt this knowledge need's content, or None."""
    content = knowledge.get("adopted_content") or {}
    if not content.get("sha256"):
        return "the knowledge need identifies no content (adopted_content with a sha256)"
    if content.get("path"):
        path = Path(content["path"]) if Path(content["path"]).is_absolute() else Path(design_path).parent / content["path"]
        if not path.is_file():
            return f"its content file {content['path']} does not exist"
        if hashlib.sha256(path.read_bytes()).hexdigest() != content["sha256"]:
            return f"its content file {content['path']} no longer matches the recorded sha256"
    return None


def decision_logic_authority(actors, decision):
    """Who must adopt a recommendation's or ranking's logic: the most specialised role among the decision makers."""
    roles = {role for actor_id in decision.get("decision_makers", []) for role in actors.get(actor_id, {}).get("roles", [])}
    for authority in ("accountable_professional", "domain_expert"):
        if authority in roles:
            return authority
    return "owner"


def specialist_answer_state(book, rulings, entry, authority):
    """An answer that needs a specialist binds only under a ruling by that authority that names it."""
    candidates = [r for r in rulings.values() if entry in (r.get("scope") or [])]
    if not candidates:
        return f"awaiting a ruling by {authority}; none names it"
    for ruling in candidates:
        state, _finding = book.state(ruling["id"], entry, authority)
        if state == "recorded as ruled":
            return state
    return f"awaiting a ruling by {authority} (`{candidates[0]['id']}`)"


def resolves_in(document, dotted):
    """The value at a dotted path of mapping keys from the document root, e.g. build_profile.access, or None."""
    node = document
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def text_of(element):
    parts = []
    for key in ("text", "content", "statement", "description", "title"):
        value = element.get(key)
        if isinstance(value, str):
            parts.append(value)
    return " ".join(" ".join(parts).split())


def check_traces(design, walker, spec, spec_walker, account):
    """Rules that relate the design record to the specification."""
    findings = []
    spec_ids = spec_walker.ids
    by_id = {obj.get("id"): obj for items in spec_walker.objects.values() for _path, obj in items
             if isinstance(obj, dict) and isinstance(obj.get("id"), str)}
    placeholders = {i for i, obj in by_id.items() if obj.get("standing") == "TBD"}
    if design.get("app") != (spec.get("app") or {}).get("id"):
        findings.append(f"ERROR D-SYNC3 design app `{design.get('app')}` differs from specification app `{(spec.get('app') or {}).get('id')}`")

    traced = {}
    for path, value, owner, slot in walker.spec_refs:
        head = value.split(".")[0]
        if head not in spec_ids:
            if resolves_in(spec, value) in (None, "", [], {}):
                findings.append(f"ERROR D-T1 {path} -> `{value}`: neither an element id nor a non-empty path in the specification")
            continue
        traced.setdefault(head, []).append((owner, slot))
        expected = TRACE_CLASSES.get((owner, slot))
        if expected and "." not in value and not expected.intersection(spec_walker.parents(spec_ids[head][0])):
            findings.append(f"WARN D-T2 {path} -> `{value}` is {spec_ids[head][0]}; expected one of {sorted(expected)}")

    for need in objects(walker, "InformationNeed"):
        answers = need.get("answered_by", [])
        if not answers:
            findings.append(f"ERROR D-Q1 need `{need['id']}` is answered by no specification element")
        for value in answers:
            head = value.split(".")[0]
            if head in spec_ids and not VIEW_LIKE.intersection(spec_walker.parents(spec_ids[head][0])):
                findings.append(f"WARN D-Q2 need `{need['id']}` is answered by `{value}`, a {spec_ids[head][0]} that users do not see")

    supporting = {s["element"].split(".")[0] for s in design.get("supporting", []) or []}
    for cls, items in spec_walker.objects.items():
        if "View" not in spec_walker.parents(cls) or cls == "View":
            continue
        for _path, view in items:
            if view.get("id") not in traced and view.get("id") not in supporting:
                findings.append(f"WARN D-V1 view `{view.get('id')}` traces to no need and is not listed as supporting")

    for decision in objects(walker, "Decision"):
        if not decision.get("consequences_shown_by"):
            findings.append(f"ERROR D-DC1 decision `{decision['id']}`: no specification element shows its consequences")
    for alternative in objects(walker, "Alternative"):
        if not alternative.get("realized_by"):
            findings.append(f"ERROR D-AL1 alternative `{alternative['id']}` is realised by no scenario, series or category")
    decided_concerns = {c for d in objects(walker, "Decision") for c in d.get("concerns", [])}
    for concern in objects(walker, "Concern"):
        if concern["id"] in decided_concerns and not concern.get("measured_by") and concern.get("measure_kind") != "qualitative":
            findings.append(f"WARN D-O1 concern `{concern['id']}` informs a decision but is measured by nothing")

    non_uses_in_spec = [" ".join(s.split()) for s in ((spec.get("purpose") or {}).get("non_uses") or [])]
    for non_use in objects(walker, "NonUse"):
        if non_use.get("disclose") is False:
            continue
        shown = non_use.get("disclosed_by", [])
        if not shown:
            findings.append(f"ERROR D-NU1 non-use `{non_use['id']}` must be disclosed, but no element discloses it")
            continue
        statement = " ".join(non_use["statement"].split())
        texts = [text_of(by_id[v.split(".")[0]]) for v in shown if v.split(".")[0] in by_id]
        if statement not in non_uses_in_spec and not any(statement in t for t in texts):
            findings.append(f"WARN D-NU1 non-use `{non_use['id']}`: its statement does not appear verbatim in the disclosing elements or purpose.non_uses")

    open_gap_targets = account["open_gap_targets"]

    def only_placeholders(values):
        heads = [v.split(".")[0] for v in values]
        return bool(heads) and all(h in placeholders for h in heads)

    for knowledge in objects(walker, "KnowledgeNeed"):
        supplied = knowledge.get("satisfied_by", [])
        if (not supplied or only_placeholders(supplied)) and knowledge["id"] not in open_gap_targets:
            findings.append(f"ERROR D-K1 knowledge need `{knowledge['id']}` is satisfied by nothing, or only by placeholders, and no open gap records it")
    for holding in objects(walker, "DataHolding"):
        if holding.get("availability") in ("available", "obtainable") and not holding.get("realized_by"):
            findings.append(f"WARN D-DH1 data holding `{holding['id']}` is available but realised by no data source")
    for obligation in objects(walker, "Obligation"):
        addressed = obligation.get("addressed_by", [])
        if addressed and only_placeholders(addressed) and obligation["id"] not in open_gap_targets:
            findings.append(f"WARN D-OB1 obligation `{obligation['id']}` is addressed only by placeholders and no open gap records it")
            account["unaddressed"].append(obligation["id"])

    tier = (design.get("tier") or {}).get("tier")
    spec_tier = (spec.get("consequence") or {}).get("tier")
    if tier and spec_tier and tier != spec_tier:
        findings.append(f"ERROR D-SYNC1 design tier `{tier}` differs from specification tier `{spec_tier}`")
    needs = {n["id"]: n for n in objects(walker, "InformationNeed")}
    for question in ((spec.get("purpose") or {}).get("questions") or []):
        need = needs.get(question.get("id"))
        if need is None:
            findings.append(f"ERROR D-SYNC2 specification question `{question.get('id')}` has no information need of the same id")
        elif " ".join(question.get("text", "").split()) != " ".join(need["question"].split()):
            findings.append(f"ERROR D-SYNC2 specification question `{question.get('id')}` differs from the need's wording")
    return findings


def coverage_table(walker, account):
    options = {o["id"]: o for o in objects(walker, "DesignOption")}
    chosen = {}
    for choice in objects(walker, "DesignChoice"):
        option = options.get(choice.get("selects"), {})
        for need_id in option.get("for_needs", []) + option.get("for_decisions", []):
            chosen.setdefault(need_id, []).append((option.get("pattern") or "-", account["binding"].get(choice["id"], "-")))
    rows = ["| Need or decision | Task (query/target/cardinality) or role | Chosen pattern | Choice: category; as recorded | Answered by |", "|---|---|---|---|---|"]
    for need in objects(walker, "InformationNeed"):
        picks = chosen.get(need["id"], [("none", "-")])
        rows.append(f"| `{need['id']}` | {task_text(need.get('task') or {})} | {', '.join(p for p, _ in picks)} | {', '.join(b for _, b in picks)} | {', '.join(need.get('answered_by', [])) or '-'} |")
    for decision in objects(walker, "Decision"):
        picks = chosen.get(decision["id"], [("none", "-")])
        rows.append(f"| `{decision['id']}` | {decision['app_role']} | {', '.join(p for p, _ in picks)} | {', '.join(b for _, b in picks)} | {', '.join(decision.get('consequences_shown_by', [])) or '-'} |")
    return rows


def run(schemas_dir, catalogue_path, design_path, spec_path):
    schemas = {}
    for name in ("app-design", "app-patterns", "app-spec"):
        path = Path(schemas_dir) / f"{name}.schema.json"
        schemas[name] = json.loads(path.read_text(encoding="utf-8"))
    report = ["# check_design report", "", f"## {design_path}", "", "DOCUMENTS"]
    catalogue = load_document(catalogue_path, schemas["app-patterns"], "PatternCatalogue", "catalogue", report)
    design = load_document(design_path, schemas["app-design"], "AppDesign", "design", report)
    spec = load_document(spec_path, schemas["app-spec"], "AppSpec", "specification", report) if spec_path else None
    if catalogue is None or design is None or (spec_path and spec is None):
        report.append("\nVERDICT: documents did not parse or validate; no rules were run.")
        return "\n".join(report), 1

    catalogue_walker = walk(schemas["app-patterns"], catalogue, "PatternCatalogue")
    design_walker = walk(schemas["app-design"], design, "AppDesign", DesignWalker)
    patterns = {p["id"]: p for p in catalogue.get("patterns", []) or []}
    findings = check_catalogue(catalogue, catalogue_walker, schemas["app-spec"]["$defs"])
    design_findings, account = check_design(design, design_walker, patterns, design_path)
    findings += design_findings
    trace_findings = []
    if spec is not None:
        spec_walker = walk(schemas["app-spec"], spec, "AppSpec")
        trace_findings = check_traces(design, design_walker, spec, spec_walker, account)
    findings += trace_findings
    trace_complete = not [f for f in trace_findings if f.startswith("ERROR")]

    errors = [f for f in findings if f.startswith("ERROR")]
    warnings = [f for f in findings if f.startswith("WARN")]
    report.append(f"\nRULES: {len(errors)} errors, {len(warnings)} warnings")
    report.extend(f"- {f}" for f in errors + warnings)

    report.append("\nCOVERAGE")
    report.extend(coverage_table(design_walker, account))

    pending = {c: b for c, b in account["binding"].items() if "recorded as ruled" not in b}
    counts = account["counts"]
    report.append("\nAS RECORDED (the checker reads the record; it cannot establish that a person made a ruling)")
    report.append(f"- choices: {len(account['binding'])} ({len(account['binding']) - len(pending)} recorded as ruled; {len(pending)} not)")
    report.extend(f"  - `{choice_id}`: {state}" for choice_id, state in pending.items())
    report.append(f"- answers that need a specialist's ruling and lack it: {len(account['specialist'])}")
    report.extend(f"  - `{entry}`: {state}" for entry, state in account["specialist"].items())
    report.append(f"- decisions whose recommendation or ranking logic is not recorded as adopted: {len(account['unadopted'])}")
    report.extend(f"  - `{d}`: {state}" for d, state in account["unadopted"].items())
    report.append(f"- needs and decisions without a choice: {', '.join(f'`{i}`' for i in account['unchosen']) or 'none'}")
    report.append(f"- authoring questions: {counts['asked']} asked; {counts['answered']} answered; "
                  f"{counts['open_gaps']} open gaps; {counts['ruled_around']} ruled around; "
                  f"{sum(len(v) for v in account['unanswered'].values())} unaddressed")
    report.extend(f"  - unaddressed in `{choice_id}`: {', '.join(keys)}" for choice_id, keys in account["unanswered"].items())
    report.append(f"- consequence tier: {account['tier']}")
    report.append(f"- obligations not addressed: {', '.join(f'`{o}`' for o in account['unaddressed']) or 'none'}")
    report.append(f"- obligations met only by a human act, carried as acceptance conditions: {', '.join(f'`{o}`' for o in account['conditions']) or 'none'}")
    ruled_around = [g["id"] for g in account["gaps"].values()
                    if g.get("status") == "ruled_around" and g["id"] in account["ruled_gaps"]]
    open_gaps = [g for g in account["gaps"].values()
                 if g.get("status") == "open" or (g.get("status") == "ruled_around" and g["id"] not in ruled_around)]
    blocking = [g["id"] for g in open_gaps if set(g.get("blocking", [])) - {"none"}]
    report.append(f"- open design gaps: {len(open_gaps)} ({len(blocking)} blocking: {', '.join(f'`{g}`' for g in blocking) or 'none'}); ruled around: {', '.join(f'`{g}`' for g in ruled_around) or 'none'}")

    ruled = (not errors and not pending and not account["specialist"] and not account["unadopted"]
             and not account["unchosen"] and not account["unanswered"] and not account["unaddressed"]
             and account["tier"] == "recorded as ruled")
    if not ruled:
        state = "NOT RULED"
    elif open_gaps:
        state = f"RULED WITH OPEN GAPS ({', '.join(blocking) or 'none blocking'})"
    elif ruled_around:
        state = "RULED WITH GAPS RULED AROUND"
    else:
        state = "RULED"
    trace_verdict = "" if spec is None else f"; trace to the specification {'COMPLETE' if trace_complete else 'INCOMPLETE'}"
    report.append(f"\nVERDICT: design {state}, as recorded{trace_verdict}. The checker reads records; whether a person made "
                  "each ruling is shown by the decision record, not by this check. A ruled, fully traced design is not "
                  "thereby right or adequate; acceptance is the owner's.")
    extensions = design_walker.extensions
    report.append(f"\nEXTENSIONS in the design record: {len(extensions)}")
    report.extend(f"- `{path}`: {check_spec.summarize(value)}" for path, value in extensions)
    return "\n".join(report), 1 if errors else 0


def main(argv):
    args = argv[1:]
    if args[:1] == ["--digest"]:
        if len(args) != 3:
            print(__doc__)
            return 2
        design = read_yaml(args[2])
        ruling = next((r for r in design.get("rulings", []) or [] if r.get("id") == args[1]), None)
        if ruling is None:
            print(f"no ruling `{args[1]}` in {args[2]}")
            return 1
        print(f"Digest {args[1]}: {ruling_digest(design, ruling)}")
        return 0
    try:
        schemas_dir = args[args.index("--schemas") + 1]
        catalogue_path = args[args.index("--catalogue") + 1]
    except (ValueError, IndexError):
        print(__doc__)
        return 2
    spec_path = None
    if "--spec" in args:
        position = args.index("--spec")
        if position + 1 >= len(args):
            print(__doc__)
            return 2
        spec_path = args[position + 1]
    consumed = {"--schemas", schemas_dir, "--catalogue", catalogue_path}
    if spec_path:
        consumed |= {"--spec", spec_path}
    designs = [a for a in args if a not in consumed]
    if len(designs) != 1:
        print(__doc__)
        return 2
    text, status = run(schemas_dir, catalogue_path, designs[0], spec_path)
    print(text)
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv))
