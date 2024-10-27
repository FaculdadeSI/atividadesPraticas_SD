document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const id = urlParams.get("id"); // Obtenha o ID da URL

  // Lógica para buscar o registro usando o ID
  fetch(`/query?id=${id}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Erro na resposta da rede");
      }
      return response.json();
    })
    .then((data) => {
      if (data.error) {
        alert(data.error);
        window.location.href = "/";
      } else {
        document.getElementById(
          "record-details"
        ).innerText = `Nome: ${data.name}, Email: ${data.email}, CPF: ${data.CPF}`;

        // Preencher os campos do formulário de atualização com os dados do registro
        document.querySelector("#update-form [name=id]").value = data.id; // Para o formulário de atualização
        document.querySelector("#update-form [name=name]").value = data.name;
        document.querySelector("#update-form [name=email]").value = data.email;
        document.querySelector("#update-form [name=CPF]").value = data.CPF;

        // Acessível aqui para a exclusão
        setupDeleteButton(id); // Passa o id para a função que configura o botão de delete
      }
    })
    .catch((error) => console.error("Erro ao buscar registro:", error));
});

// Função para configurar a lógica de exclusão
function setupDeleteButton(id) {
  document.getElementById("delete-btn").addEventListener("click", () => {
    // Pergunta de confirmação
    const confirmDelete = confirm(
      "Você tem certeza que deseja excluir este registro?"
    );
    if (!confirmDelete) {
      return; // Se o usuário não confirmar, sai da função
    }

    fetch(`/delete`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id }), // Envie o ID para a exclusão
    })
      .then((response) => {
        if (response.ok) {
          alert("Registro excluído com sucesso!");
          window.location.href = "/"; // Redireciona para a página inicial
        } else {
          throw new Error("Erro ao excluir o registro.");
        }
      })
      .catch((error) => console.error("Erro:", error));
  });
}

// Lógica para atualizar o registro
document
  .getElementById("update-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const record = Object.fromEntries(formData.entries());

    // Verifica se todos os campos foram preenchidos
    if (!record.name || !record.email || !record.CPF) {
      alert("Por favor, preencha todos os campos.");
      return;
    }

    // Obtém os dados antigos do registro
    const oldName = document.querySelector("#update-form [name=name]").dataset
      .oldValue;
    const oldEmail = document.querySelector("#update-form [name=email]").dataset
      .oldValue;
    const oldCPF = document.querySelector("#update-form [name=CPF]").dataset
      .oldValue;

    // Checa se todos os dados novos são diferentes dos antigos
    if (
      record.name === oldName ||
      record.email === oldEmail ||
      record.CPF === oldCPF
    ) {
      alert("Todos os novos dados devem ser diferentes dos antigos.");
      return;
    }

    fetch("/update", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(record),
    })
      .then((response) => response.json())
      .then((data) => {
        alert("Registro atualizado com sucesso!");
        location.reload();
      })
      .catch((error) => console.error("Erro ao atualizar registro:", error));
  });
