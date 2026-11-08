"""B-only, read-only AX readiness/traversal around the maintained primitives.

Application self-references are observations, never replacement windows. No
activation, reopen or synthetic UI event is introduced by this wrapper.
"""

MAIN_TITLE = 'Chirality App v4 — walking skeleton'
MAX_WINDOW_REFERENCES = 32
MAX_NODES = 900  # Preserve the maintained walk's strict len(rows) < 900.
MAX_DEPTH = 20
MAX_EDGES = 1800  # Bound even a malformed graph of repeated references.
PROPERTIES = ('AXRole', 'AXTitle', 'AXDescription', 'AXValue', 'AXEnabled')


class MainWindowUnavailable(RuntimeError):
    """No distinct owned main window has been observed yet."""


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def wrap_ax(BaseAX):
    class BAX(BaseAX):
        def _same(self, left, right):
            return bool(self.c.CFEqual(left, right))

        def _window_roots(self):
            raw = BaseAX.windows(self)
            require(isinstance(raw, list) and len(raw) <= MAX_WINDOW_REFERENCES,
                    'unexpected AX window-reference expansion')
            seen, admitted, observations = [], [], []
            for element in raw:
                self.own(element)
                props = {name: self.attr(element, name) for name in ('AXRole', 'AXSubrole', 'AXTitle')}
                if self._same(element, self.app):
                    disposition = 'application-self-reference'
                elif any(self._same(element, old) for old in seen):
                    disposition = 'duplicate-reference'
                elif props['AXRole'] not in ('AXWindow', 'AXDialog', 'AXSheet'):
                    disposition = 'not-a-window-root'
                else:
                    disposition = 'owned-window-root'
                    admitted.append(element)
                seen.append(element)
                observations.append({**props, 'disposition': disposition})
            self.last_window_observation = observations
            self._admitted_window_roots = admitted
            return admitted

        def window_observation(self):
            self._window_roots()
            return list(self.last_window_observation)

        def windows(self):
            return self._window_roots()

        def main_if_available(self):
            matches = [element for element in self.windows()
                       if self.attr(element, 'AXRole') == 'AXWindow'
                       and self.attr(element, 'AXTitle') == MAIN_TITLE]
            require(len(matches) <= 1, 'owned main window ambiguous')
            return matches[0] if matches else None

        def main(self):
            element = self.main_if_available()
            if element is None:
                raise MainWindowUnavailable('distinct owned main AXWindow unavailable')
            return element

        def walk(self, element, depth=0, web=False):
            # Track CF equality, not Python pointer identity: aliases can be
            # different local references to the same remote AX object.
            require(type(depth) is int and 0 <= depth <= MAX_DEPTH and type(web) is bool,
                    'invalid AX traversal context')
            rows, seen = [], []
            stack = [(element, depth, web, ())]
            edges = 0
            notes = {'cycles_pruned': 0, 'duplicate_references_pruned': 0,
                     'application_boundaries_pruned': 0, 'window_boundaries_pruned': 0}
            self.last_walk_observation = notes
            while stack:
                current, level, in_web, ancestors = stack.pop()
                edges += 1
                require(edges <= MAX_EDGES, 'unexpected AX reference expansion')
                self.own(current)
                if any(self._same(current, ancestor) for ancestor in ancestors):
                    notes['cycles_pruned'] += 1
                    continue
                require(level <= MAX_DEPTH, 'unexpected AX depth')
                if self._same(current, self.app):
                    notes['application_boundaries_pruned'] += 1
                    continue
                props = {name: self.attr(current, name) for name in PROPERTIES}
                if props['AXRole'] == 'AXApplication':
                    notes['application_boundaries_pruned'] += 1
                    continue
                another_root = any(self._same(current, root) for root in
                                   getattr(self, '_admitted_window_roots', ()))
                if not self._same(current, element) and (another_root or props['AXRole'] in ('AXWindow', 'AXMenuBar')):
                    notes['window_boundaries_pruned'] += 1
                    continue
                in_web = in_web or props['AXRole'] == 'AXWebArea'
                previous = next((old_web for old, old_web in seen if self._same(current, old)), None)
                if previous is not None:
                    require(previous == in_web, 'AX reference crosses native/Web boundary')
                    notes['duplicate_references_pruned'] += 1
                    continue
                seen.append((current, in_web))
                rows.append((current, props, in_web))
                require(len(rows) < MAX_NODES, 'unexpected AX expansion')
                children = self.attr(current, 'AXChildren') or []
                require(isinstance(children, list) and len(children) < MAX_NODES,
                        'unexpected AX child expansion')
                for child in reversed(children):
                    stack.append((child, level + 1, in_web, (*ancestors, current)))
            notes['unique_nodes'] = len(rows)
            notes['references_checked'] = edges
            return rows

    return BAX
