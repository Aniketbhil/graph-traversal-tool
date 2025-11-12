# 🧭 Graph Traversal Tool (BFS & DFS Visualizer)

A full-stack web application that demonstrates **Breadth-First Search (BFS)** and **Depth-First Search (DFS)** graph traversals.

- **Frontend:** React + Vite  
- **Backend:** Flask (Python)  
- **Purpose:** Explore connectivity in graphs represented by adjacency lists or matrices.

---

## 🚀 Features

- Interactive input for vertices and edges  
- Choose adjacency **List** or **Matrix** representation  
- Run **BFS** or **DFS** and view traversal order  
- Works with letter-labeled nodes (`A, B, C, D, …`)  
- Flask REST API for algorithm logic  
- Clean React UI for user interaction  

---

## 🧱 Project Structure
```bash
graph-traversal-tool/
│
├── backend/
│ ├── app.py # Flask API
│ ├── requirements.txt # Python dependencies
│
└── frontend/
├── src/
│ ├── App.jsx # Main React component
│ ├── index.jsx
│ └── index.css
├── vite.config.js
└── package.json
```


---

## ⚙️ How to Run Locally

### 1️⃣ Backend (Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py

The backend will start at http://localhost:5000
```


2️⃣ Frontend (React)

Open another terminal:
```bash
cd frontend
npm install
npm run dev

The frontend will start at http://localhost:5173

Make sure Flask is running first; the React app fetches data from it.

```

🧩 Example Input

Vertices: 5
Edges:
A B
A C
B D
C E
Start: A

BFS Output: A → B → C → D → E
DFS Output: A → B → D → C → E


🧠 Concepts Demonstrated

1. Graph traversal algorithms

2. Queue vs. recursion mechanics

3. Adjacency list & matrix representations

4. Frontend ↔ Backend API communication

🛠️ Tech Stack

| Layer      | Technology              |
| ---------- | ----------------------- |
| Frontend   | React, Vite, JavaScript |
| Backend    | Python, Flask           |
| Styling    | CSS                     |
| API Format | JSON                    |

🤝 Contributing

1. Fork this repository

2. Create a feature branch (git checkout -b new-feature)

3. Commit your changes (git commit -m "Add new feature")

4. Push to your branch (git push origin new-feature)

5. Open a Pull Request

Made with ❤️ by Aniket 