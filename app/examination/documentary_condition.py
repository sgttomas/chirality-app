"""Selected documentary meaning; independent of exact artifact/publication identities."""
import hashlib
import json
from pathlib import Path
import re

METHOD = 'selected-documentary-source-condition/v2'


def project(raw, selectors):
    lines = raw.decode('utf-8').splitlines(keepends=True)
    output = b''
    for selector in selectors:
        if 'heading' in selector:
            heading = selector['heading']
            hits = [i for i, line in enumerate(lines) if line.rstrip('\r\n') == heading]
            if len(hits) != 1:
                raise ValueError('documentary heading missing or repeated: ' + heading)
            start = hits[0]
            level = len(heading) - len(heading.lstrip('#'))
            end = next((i for i in range(start + 1, len(lines))
                        if re.match(r'^#{1,' + str(level) + r'} ', lines[i])), len(lines))
            selected = ''.join(lines[start:end])
        elif 'case' in selector:
            key = selector['case']
            hits = [line for line in lines if re.match(r'^\| ' + re.escape(key) + r'\b', line)]
            if len(hits) != selector['count']:
                raise ValueError('documentary case missing or repeated: ' + key)
            rows = []
            for line in hits:
                cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
                trim = selector.get('trim_observation')
                if trim:
                    cells[trim['column']] = cells[trim['column']].split(trim['marker'], 1)[0].rstrip()
                columns = selector.get('columns', range(len(cells)))
                rows.append('|'.join(cells[column] for column in columns))
            selected = '\n'.join(rows)
        else:
            prefix = selector['paragraphPrefix']
            hits = [i for i, line in enumerate(lines) if line.startswith(prefix)]
            if len(hits) != selector.get('count', 1):
                raise ValueError('documentary clause missing or repeated: ' + prefix)
            parts = []
            for start in hits:
                if prefix.startswith(('- **', '**')):
                    # Complete named clause, including continuation paragraphs.
                    end = next((i for i in range(start + 1, len(lines))
                                if lines[i].startswith(('- **', '**', '#', '| '))), len(lines))
                else:
                    end = next((i for i in range(start + 1, len(lines)) if not lines[i].strip()), len(lines))
                parts.append(''.join(lines[start:end]))
            selected = ''.join(parts)
        data = selected.encode('utf-8')
        output += len(data).to_bytes(8, 'big') + data
    return output


class Condition:
    def __init__(self, root, manifest_bytes, read_source):
        self.root = Path(root)
        self.raw = manifest_bytes
        self.read_source = read_source
        self.manifest = json.loads(manifest_bytes)
        if self.manifest['method'] != METHOD:
            raise ValueError('unknown documentary source condition')

    def capture(self, group):
        captured = {}
        extent = []
        for source in self.manifest['sources']:
            if group not in source['groups']:
                continue
            raw = self.read_source(self.root, source['path'])
            actual = hashlib.sha256(project(raw, source['selectors'])).hexdigest()
            if actual != source['sha256']:
                raise ValueError('documentary meaning changed: ' + source['path'])
            captured[source['path']] = raw
            extent.append({'path': source['path'], 'selectors': source['selectors'], 'sha256': actual})
        if not extent:
            raise ValueError('unknown or empty documentary source group')
        return captured, {'method': METHOD, 'manifest_sha256': hashlib.sha256(self.raw).hexdigest(),
                          'checked_extent': extent, 'standing': 'checked at this read; producer use unverified',
                          'authority_authenticated': False}
