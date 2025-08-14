const API_URL = "http://127.0.0.1:5000/tarefas";

// Carregar tarefas ao iniciar
window.onload = listarTarefas;

function listarTarefas() {
    fetch(API_URL)
        .then(res => res.json())
        .then(tarefas => {
            const lista = document.getElementById("lista");
            lista.innerHTML = "";
            tarefas.forEach(tarefa => {
                const li = document.createElement("li");

                li.innerHTML = `
                    <input type="checkbox" ${tarefa.concluida ? "checked" : ""} onchange="atualizarTarefa(${tarefa.id}, this.checked)">
                    ${tarefa.descricao}
                    <button onclick="removerTarefa(${tarefa.id})">❌</button>
                `;

                lista.appendChild(li);
            });
    });
}

function adicionarTarefa() {
    const tarefa = document.getElementById("tarefa").value;
    if (!tarefa) return alert("Digite uma tarefa!");

    fetch(API_URL, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({tarefa})
    }).then(() => {
        document.getElementById("tarefa").value = "";
        listarTarefas();
    });
}

function atualizarTarefa(id, concluida) {
    fetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({concluida})
    }).then(listarTarefas);
}

function removerTarefa(id) {
    fetch(`${API_URL}/${id}`, {method: "DELETE"})
        .then(listarTarefas);
}
