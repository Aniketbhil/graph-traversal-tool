import React, { useEffect, useRef } from "react";
import { Network } from "vis-network";

export default function GraphVisualizer({ edges, order }) {
  const containerRef = useRef(null);
  const networkRef = useRef(null);

  // Parse edges (A B)
  const nodesSet = new Set();
  const edgeList = [];

  edges.split("\n").forEach((line) => {
    const p = line.trim().split(" ");
    if (p.length === 2) {
      const [u, v] = p;
      nodesSet.add(u);
      nodesSet.add(v);
      edgeList.push({ from: u, to: v });
    }
  });

  const nodeArray = Array.from(nodesSet);

  // ★ FIXED POSITIONING (NO MOVING OUT OF SCREEN)
  const nodes = nodeArray.map((node, i) => ({
    id: node,
    label: node,
    x: i * 120,           // horizontal spacing
    y: 0,                 // same vertical line
    fixed: { x: true, y: true },  // ★ prevents moving
    shape: "circle",
    size: 25,
    color: "#60a5fa",
    font: { color: "#000", size: 20 }
  }));

  useEffect(() => {
    if (!containerRef.current) return;

    const data = {
      nodes,
      edges: edgeList
    };

    const options = {
      physics: { enabled: false },    // no movement at all
      interaction: {
        dragNodes: false,             // user can't drag nodes
        dragView: true,
        zoomView: true
      },
      edges: {
        arrows: { to: { enabled: true } },
        smooth: false
      }
    };

    networkRef.current = new Network(containerRef.current, data, options);

    // ★ Center the graph inside the screen
    networkRef.current.moveTo({
      position: { x: (nodes.length * 120) / 2, y: 0 },
      scale: 0.8
    });

  }, [edges]);

  // BFS/DFS Highlight Animation
  useEffect(() => {
    if (!order || order.length === 0 || !networkRef.current) return;

    let i = 0;
    const interval = setInterval(() => {
      const node = order[i];
      networkRef.current.selectNodes([node]);
      networkRef.current.focus(node, { scale: 1 });

      i++;
      if (i >= order.length) clearInterval(interval);
    }, 800);

    return () => clearInterval(interval);
  }, [order]);

  return (
    <div
      ref={containerRef}
      style={{
        height: "500px",
        width: "100%",
        background: "#fff",
        borderRadius: 8,
        border: "1px solid #ccc",
        overflow: "hidden"
      }}
    />
  );
}
