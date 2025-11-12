from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import deque
import string

app = Flask(__name__)
CORS(app)

# Generate label map: A, B, C, ...
def letter_labels(n):
    return list(string.ascii_uppercase[:n])

def build_graph_from_input(vertices, representation, edges_text):
    n = int(vertices)
    labels = letter_labels(n)
    label_to_index = {label: i for i, label in enumerate(labels)}

    lines = [line.strip() for line in edges_text.split('\n') if line.strip()]

    if representation == 'list':
        g = {label: [] for label in labels}
        for line in lines:
            parts = line.split()
            if len(parts) < 2:
                continue
            a, b = parts[0].upper(), parts[1].upper()
            if b not in g[a]:
                g[a].append(b)
            if a not in g[b]:
                g[b].append(a)
        return g
    else:
        mat = [[0] * n for _ in range(n)]
        for line in lines:
            parts = line.split()
            if len(parts) < 2:
                continue
            a, b = parts[0].upper(), parts[1].upper()
            i, j = label_to_index[a], label_to_index[b]
            mat[i][j] = 1
            mat[j][i] = 1
        return mat, labels, label_to_index


@app.route('/traverse', methods=['POST'])
def traverse():
    data = request.get_json()
    vertices = int(data.get('vertices'))
    rep = data.get('representation')
    edges = data.get('edges', '')
    start = data.get('start', 'A').upper()
    t = data.get('type', 'bfs')

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


# BFS for adjacency list
def bfs_list(graph, start):
    visited = {v: False for v in graph}
    q = deque([start])
    visited[start] = True
    order, steps = [], []

    while q:
        v = q.popleft()
        order.append(v)
        neighbors = sorted(graph[v])
        steps.append({'node': v, 'neighbors': neighbors})
        for nb in neighbors:
            if not visited[nb]:
                visited[nb] = True
                q.append(nb)

    return order, steps


# DFS for adjacency list
def dfs_list(graph, start):
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


# BFS for adjacency matrix
def bfs_matrix(mat, labels, label_to_index, start):
    n = len(labels)
    visited = [False] * n
    q = deque([label_to_index[start]])
    visited[label_to_index[start]] = True
    order, steps = [], []

    while q:
        idx = q.popleft()
        label = labels[idx]
        order.append(label)
        neighbors = [
            labels[i] for i, val in enumerate(mat[idx]) if val == 1
        ]
        steps.append({'node': label, 'neighbors': neighbors})
        for nb_label in neighbors:
            nb_idx = label_to_index[nb_label]
            if not visited[nb_idx]:
                visited[nb_idx] = True
                q.append(nb_idx)

    return order, steps


# DFS for adjacency matrix
def dfs_matrix(mat, labels, label_to_index, start):
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



if __name__ == '__main__':
    app.run(debug=True)
