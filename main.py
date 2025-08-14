from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# --- Criar tabela se não existir ---
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        concluida BOOLEAN NOT NULL DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

init_db()

# --- Listar tarefas ---
@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, descricao, concluida FROM tarefas")
    tarefas = [{"id": row[0], "descricao": row[1], "concluida": bool(row[2])} for row in cursor.fetchall()]
    conn.close()
    return jsonify(tarefas)

# --- Adicionar tarefa ---
@app.route("/tarefas", methods=["POST"])
def adicionar_tarefa():
    data = request.json
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tarefas (descricao) VALUES (?)", (data["tarefa"],))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Tarefa adicionada com sucesso!"})

# --- Atualizar status ---
@app.route("/tarefas/<int:id>", methods=["PUT"])
def atualizar_tarefa(id):
    data = request.json
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET concluida = ? WHERE id = ?", (data["concluida"], id))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Tarefa atualizada com sucesso!"})

# --- Remover tarefa ---
@app.route("/tarefas/<int:id>", methods=["DELETE"])
def remover_tarefa(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Tarefa removida com sucesso!"})

if __name__ == "__main__":
    app.run(debug=True)
