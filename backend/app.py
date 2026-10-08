from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_NAME = "todos.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


@app.route("/api/todos", methods=["GET"])
def get_todos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, completed FROM todos")
    rows = cursor.fetchall()
    conn.close()

    todos = [
        {
            "id": row[0],
            "task": row[1],
            "completed": bool(row[2])
        }
        for row in rows
    ]

    return jsonify(todos)


@app.route("/api/todos", methods=["POST"])
def add_todo():
    data = request.get_json()

    if not data or "task" not in data:
        return jsonify({"error": "Task is required"}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO todos (task, completed) VALUES (?, ?)",
        (data["task"], 0)
    )
    conn.commit()

    todo_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "id": todo_id,
        "task": data["task"],
        "completed": False
    }), 201


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)