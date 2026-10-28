"""Pure graph operations; no lifecycle or approval machinery."""
from collections import defaultdict


def find_sccs(graph, nodes):
    """Iterative Kosaraju traversal, including self-loops and large graphs."""
    visited, order = set(), []
    for origin in sorted(nodes):
        if origin in visited:
            continue
        visited.add(origin)
        stack = [(origin, iter(sorted(graph.get(origin, ())))) ]
        while stack:
            node, children = stack[-1]
            child = next(children, None)
            if child is None:
                order.append(node)
                stack.pop()
            elif child not in visited:
                visited.add(child)
                stack.append((child, iter(sorted(graph.get(child, ())))))
    reverse = defaultdict(set)
    for source, targets in graph.items():
        for target in targets:
            reverse[target].add(source)
    visited, components = set(), []
    for origin in reversed(order):
        if origin in visited:
            continue
        component, stack = [], [origin]
        visited.add(origin)
        while stack:
            node = stack.pop()
            component.append(node)
            for child in sorted(reverse.get(node, ())):
                if child not in visited:
                    visited.add(child)
                    stack.append(child)
        if len(component) > 1 or origin in graph.get(origin, ()):
            components.append(sorted(component))
    return sorted(components)
