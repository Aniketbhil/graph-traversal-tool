import React, { useState } from "react";

export default function App() {
  const [vertices, setVertices] = useState(5); // number of vertices (A..)
  const [edges, setEdges] = useState("A B\nA C\nB D\nC E");
  const [representation, setRepresentation] = useState("list"); // "list" or "matrix"
  const [startNode, setStartNode] = useState("A");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  async function handleTraversal(type) {
    setErrorMsg("");
    setResult(null);

    // Basic validation
    const n = Number(vertices);
    if (!Number.isFinite(n) || n < 1 || n > 26) {
      setErrorMsg("Vertices must be a number between 1 and 26.");
      return;
    }
    if (!/^[A-Z]$/.test(startNode.toUpperCase())) {
      setErrorMsg("Start node must be a single letter like A, B, C ...");
      return;
    }

    setLoading(true);
    try {
      const payload = {
        vertices: n,
        representation,
        edges,
        start: startNode.toUpperCase(),
        type,
      };

      const res = await fetch("http://localhost:5000/traverse", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Server returned ${res.status}: ${text}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      // Friendly error message
      setErrorMsg(
        err.message.includes("Failed to fetch")
          ? "Failed to connect to backend. Is Flask running on http://localhost:5000 ? (Enable CORS with flask-cors if needed.)"
          : err.message
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Transversal Tool</h1>

      <div style={styles.grid}>
        <div style={styles.card}>
          <label style={styles.label}>
            Representation
            <select
              value={representation}
              onChange={(e) => setRepresentation(e.target.value)}
              style={styles.select}
            >
              <option value="list">Adjacency List (use letters)</option>
              <option value="matrix">Adjacency Matrix (use letters)</option>
            </select>
          </label>

          <label style={styles.label}>
            Vertices (count, A..): 
            <input
              style={styles.input}
              type="number"
              min={1}
              max={26}
              value={vertices}
              onChange={(e) => setVertices(e.target.value)}
            />
          </label>

          <label style={styles.label}>
            Start Node (letter):
            <input
              style={styles.input}
              type="text"
              maxLength={1}
              value={startNode}
              onChange={(e) => setStartNode(e.target.value.toUpperCase())}
            />
          </label>

          <label style={styles.label}>
            Edges (one per line: "A B")
            <textarea
              rows={8}
              style={styles.textarea}
              value={edges}
              onChange={(e) => setEdges(e.target.value.toUpperCase())}
            />
          </label>

          <div style={styles.buttons}>
            <button style={styles.btn} onClick={() => handleTraversal("bfs")} disabled={loading}>
              {loading ? "Running..." : "Run BFS"}
            </button>
            <button style={{ ...styles.btn, background: "#059669" }} onClick={() => handleTraversal("dfs")} disabled={loading}>
              {loading ? "Running..." : "Run DFS"}
            </button>
          </div>

          {errorMsg && <div style={styles.error}>{errorMsg}</div>}
          <div style={styles.hint}>
            Hint: Use letters A..Z for vertices. Example edges:
            <pre style={styles.pre}>A B{"\n"}A C{"\n"}B D</pre>
          </div>
        </div>

        <div style={styles.card}>
          <h3>Result</h3>
          {!result && <div style={styles.muted}>No traversal run yet.</div>}
          {result && result.error && <div style={styles.error}>{result.error}</div>}
          {result && !result.error && (
            <>
              <div><strong>Order:</strong> {JSON.stringify(result.order)}</div>
              <div style={{ marginTop: 8 }}>
                <strong>Steps:</strong>
                <pre style={styles.preSmall}>{JSON.stringify(result.steps, null, 2)}</pre>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

// Inline simple styles so you can paste without extra files
const styles = {
  container: {
    fontFamily: "Inter, system-ui, sans-serif",
    padding: 20,
    background: "#f8fafc",
    minHeight: "100vh",
  },
  title: {
    textAlign: "center",
    color: "#1e3a8a",
    marginBottom: 18,
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 16,
    maxWidth: 1100,
    margin: "0 auto",
  },
  card: {
    background: "#fff",
    padding: 16,
    borderRadius: 10,
    boxShadow: "0 6px 18px rgba(2,6,23,0.06)",
  },
  label: {
    display: "block",
    marginBottom: 8,
    fontSize: 14,
  },
  input: {
    width: 140,
    padding: "8px 10px",
    borderRadius: 6,
    border: "1px solid #d1d5db",
    display: "block",
    marginTop: 6,
  },
  select: {
    width: "100%",
    padding: "8px 10px",
    borderRadius: 6,
    border: "1px solid #d1d5db",
    marginTop: 6,
  },
  textarea: {
    width: "100%",
    padding: 8,
    borderRadius: 6,
    border: "1px solid #d1d5db",
    marginTop: 6,
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, 'Roboto Mono', monospace",
  },
  buttons: {
    display: "flex",
    gap: 10,
    marginTop: 12,
  },
  btn: {
    flex: 1,
    background: "#2563eb",
    color: "#fff",
    border: "none",
    padding: "8px 12px",
    borderRadius: 8,
    cursor: "pointer",
  },
  error: {
    marginTop: 12,
    color: "#b91c1c",
    background: "#fee2e2",
    padding: 8,
    borderRadius: 6,
  },
  hint: {
    marginTop: 10,
    fontSize: 13,
    color: "#6b7280",
  },
  pre: {
    background: "#f3f4f6",
    padding: 8,
    borderRadius: 6,
    marginTop: 6,
  },
  preSmall: {
    background: "#111827",
    color: "#f8fafc",
    padding: 12,
    borderRadius: 6,
    marginTop: 8,
    overflowX: "auto",
  },
  muted: { color: "#6b7280" },
};
