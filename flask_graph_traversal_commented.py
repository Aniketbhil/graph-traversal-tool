"""
flask_graph_traversal_commented.py

Commented version of the graph traversal Flask app.
Each function includes inline comments explaining purpose and the CS topic it illustrates.
"""

from flask import Flask, request, jsonify  # Flask web framework pieces: app, request parsing, JSON responses
from flask_cors import CORS  # Enable Cross-Origin Resource Sharing for frontend <-> backend calls
from collections import deque  # deque used as a queue for BFS (O(1) pops from left)
import string  # standard library helper to get ASCII uppercase letters

# ----------------------------
# App initialization
# ----------------------------
app = Flask(__name__)  # create Flask app; __name__ helps locate resources
CORS(app)  # enable permissive CORS for development (careful in production)


# ----------------------------
# Utility: label generation
# ----------------------------
def letter_labels(n):
    """Return first n uppercase letters: ['A', 'B', 'C', ...]

    Topic: simple utility, mapping indices to human-readable vertex labels.
    """
    return list(string.ascii_uppercase[:n])


# ----------------------------
# Graph builder / parser
# ----------------------------
def build_graph_from_input(vertices, representation, edges_text):
    """Parse input and build either an adjacency list or an adjacency matrix.

    Parameters
    - vertices: number (or string containing number) of vertices (n)
    - representation: 'list' or anything else -> matrix
    - edges_text: multiline text where each non-empty line contains an edge like "A B"

    Returns
    - if representation == 'list': returns dict {label: [neighbors...]}
    - else: returns (matrix, labels, label_to_index)

    Topics covered: parsing, adjacency list vs adjacency matrix, label-index mapping.
    """
    n = int(vertices)  # ensure integer
    labels = letter_labels(n)  # human-readable labels
    label_to_index = {label: i for i, label in enumerate(labels)}  # constant-time label -> index lookup

    # Normalize input: split into lines, strip whitespace, drop empty lines
    lines = [line.strip() for line in edges_text.split('\n') if line.strip()]

    # Build adjacency list representation
    if representation == 'list':
        # Using lists preserves insertion order and is easy to serialize for the frontend
        g = {label: [] for label in labels}
        for line in lines:
            parts = line.split()
            if len(parts) < 2:
                # skip malformed lines (defensive programming)
                continue
            a, b = parts[0].upper(), parts[1].upper()  # normalize labels

            # Add undirected edge: a <-> b
            # NOTE: membership checks (if b not in g[a]) are O(deg(a)). For large-degree vertices, consider sets.
            if b not in g[a]:
                g[a].append(b)
            if a not in g[b]:
                g[b].append(a)

        return g

    # Build adjacency matrix representation
    else:
        # matrix uses O(n^2) memory; good for dense graphs or when constant-time edge existence checks are needed
        mat = [[0] * n for _ in range(n)]
        for line in lines:
            parts = line.split()
            if len(parts) < 2:
                continue
            a, b = parts[0].upper(), parts[1].upper()
            i, j = label_to_index[a], label_to_index[b]
            mat[i][j] = 1
            mat[j][i] = 1  # undirected

        # return extras so callers can map indices back to labels
        return mat, labels, label_to_index


# ----------------------------
# API endpoint for traversal
# ----------------------------
@app.route('/traverse', methods=['POST'])
def traverse():
    """HTTP POST endpoint that accepts JSON payload describing a graph and returns traversal info.

    Expected JSON keys (examples):
    - vertices: "4" or 4
    - representation: "list" or "matrix"
    - edges: "A B\nA C\nB D"
    - start: (optional) starting label, default 'A'
    - type: 'bfs' or 'dfs' (default 'bfs')

    Returns: JSON { 'order': [...], 'steps': [...] }
    where 'steps' is useful for visualizing the algorithm progress in a frontend.

    Topics: REST API design, request parsing, delegating to algorithm implementations.
    """
    data = request.get_json()  # parse JSON payload

    # extract parameters with defaults and normalization
    vertices = int(data.get('vertices'))
    rep = data.get('representation')
    edges = data.get('edges', '')
    start = data.get('start', 'A').upper()
    t = data.get('type', 'bfs')

    # Build the chosen representation and call the corresponding traversal
    if rep == 'list':
        graph = build_graph_from_input(vertices, rep, edges)
        if t == 'bfs':
            order, steps = bfs_list(graph, start)
        else:
            order, steps = dfs_list(graph, start)
    else:
        graph, labels, label_to_index = build_graph_from_input(vertices, rep, edges)
        if t == 'bfs':
            order, steps = bfs_matrix(graph, labels, label_to_index, start)
        else:
            order, steps = dfs_matrix(graph, labels, label_to_index, start)

    return jsonify({'order': order, 'steps': steps})


# ----------------------------
# BFS on adjacency list
# ----------------------------
def bfs_list(graph, start):
    """Breadth-First Search using an adjacency list.

    Returns: (order, steps)
      - order: list of nodes in visit order
      - steps: list of dicts { node: 'X', neighbors: [...] } capturing neighbors inspected for each node.

    Complexity: O(V + E) when neighbor list iteration dominates. Uses deque for O(1) queue operations.
    """
    visited = {v: False for v in graph}  # visited map keyed by label
    q = deque([start])  # queue initialized with start label
    visited[start] = True
    order, steps = [], []

    while q:
        v = q.popleft()  # dequeue (FIFO)
        order.append(v)

        # sort neighbors for deterministic traversal order (helpful for testing and UI)
        neighbors = sorted(graph[v])
        steps.append({'node': v, 'neighbors': neighbors})

        for nb in neighbors:
            if not visited[nb]:
                visited[nb] = True
                q.append(nb)

    return order, steps


# ----------------------------
# DFS on adjacency list (recursive)
# ----------------------------
def dfs_list(graph, start):
    """Depth-First Search using recursion over adjacency list.

    Note: recursion depth may be limited by Python's recursion limit (~1000). For deep graphs use an explicit stack.
    """
    visited = {v: False for v in graph}
    order, steps = [], []

    def rec(v):
        visited[v] = True
        order.append(v)
        neighbors = sorted(graph[v])
        steps.append({'node': v, 'neighbors': neighbors})
        for nb in neighbors:
            if not visited[nb]:
                rec(nb)

    rec(start)
    return order, steps


# ----------------------------
# BFS on adjacency matrix
# ----------------------------
def bfs_matrix(mat, labels, label_to_index, start):
    """BFS that operates on an adjacency matrix.

    mat: n x n matrix where mat[i][j] == 1 indicates an edge i->j.
    labels: index -> label mapping (['A', 'B', ...])
    label_to_index: label -> index mapping

    Complexity: scanning a row to find neighbors costs O(n) per node; overall O(n^2) in dense cases.
    """
    n = len(labels)
    visited = [False] * n  # visited by index for fast array access
    start_idx = label_to_index[start]
    q = deque([start_idx])
    visited[start_idx] = True
    order, steps = [], []

    while q:
        idx = q.popleft()
        label = labels[idx]
        order.append(label)

        # find neighbor labels by scanning the matrix row
        neighbors = [labels[i] for i, val in enumerate(mat[idx]) if val == 1]
        steps.append({'node': label, 'neighbors': neighbors})

        for nb_label in neighbors:
            nb_idx = label_to_index[nb_label]
            if not visited[nb_idx]:
                visited[nb_idx] = True
                q.append(nb_idx)

    return order, steps


# ----------------------------
# DFS on adjacency matrix (recursive)
# ----------------------------
def dfs_matrix(mat, labels, label_to_index, start):
    """Recursive DFS using adjacency matrix neighbor discovery.

    Same caution about recursion depth applies.
    """
    n = len(labels)
    visited = [False] * n
    order = []
    steps = []

    def rec(idx):
        visited[idx] = True
        label = labels[idx]
        order.append(label)

        neighbors = [labels[i] for i, val in enumerate(mat[idx]) if val == 1]
        steps.append({'node': label, 'neighbors': neighbors})

        for nb_label in neighbors:
            nb_idx = label_to_index[nb_label]
            if not visited[nb_idx]:
                rec(nb_idx)

    rec(label_to_index[start])
    return order, steps


# ----------------------------
# Run server guard
# ----------------------------
if __name__ == '__main__':
    # debug=True enables auto-reload and helpful error pages during development
    # Do not use debug=True in production (security risk).
    app.run(debug=True)
