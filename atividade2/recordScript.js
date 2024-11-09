// Constantes para URLs e mensagens
const API_URLS = {
  query: "/query",
  delete: "/delete",
  update: "/update",
  updatePartial: "/updatePartial",
};

const MESSAGES = {
  deleteConfirmation: "Você tem certeza que deseja excluir este registro?",
  deleteSuccess: "Registro excluído com sucesso!",
  updateSuccess: "Registro atualizado com sucesso!",
  partialUpdateSuccess: "Registro atualizado parcialmente com sucesso!",
  emptyFields: "Por favor, preencha todos os campos.",
  sameData: "Todos os novos dados devem ser diferentes dos antigos.",
  networkError: "Erro na resposta da rede",
};

// Função para buscar o registro com base no ID
async function fetchRecordById(id) {
  const response = await fetch(`${API_URLS.query}?id=${id}`);
  if (!response.ok) throw new Error(MESSAGES.networkError);
  return response.json();
}

// Função para preencher os detalhes do registro na tela
function displayRecordDetails(data) {
  document.getElementById(
    "record-details"
  ).innerText = `Nome: ${data.name}, Email: ${data.email}, CPF: ${data.CPF}`;
  document.querySelector("#update-form [name=id]").value = data.id;
  document.querySelector("#update-partial-form [name=id]").value = data.id;
  document.querySelector("#update-form [name=name]").value = data.name;
  document.querySelector("#update-form [name=email]").value = data.email;
  document.querySelector("#update-form [name=CPF]").value = data.CPF;
}

// Função para configurar o botão de exclusão
function setupDeleteButton(id) {
  document.getElementById("delete-btn").addEventListener("click", async () => {
    const confirmDelete = confirm(MESSAGES.deleteConfirmation);
    if (!confirmDelete) return;

    try {
      const response = await fetch(API_URLS.delete, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id }),
      });

      if (!response.ok) throw new Error("Erro ao excluir o registro.");
      alert(MESSAGES.deleteSuccess);
      window.location.href = "/";
    } catch (error) {
      console.error("Erro:", error);
    }
  });
}

// Função para atualizar o registro
async function updateRecord(record) {
  const response = await fetch(API_URLS.update, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(record),
  });
  return response.json();
}

// Função para atualizar parcialmente o registro
async function updatePartialRecord(record) {
  const response = await fetch(API_URLS.updatePartial, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(record),
  });
  return response.json();
}

// Função para validar os dados do formulário
function validateForm(record, oldValues) {
  if (!record.name || !record.email || !record.CPF) {
    alert(MESSAGES.emptyFields);
    return false;
  }

  if (
    record.name === oldValues.name ||
    record.email === oldValues.email ||
    record.CPF === oldValues.CPF
  ) {
    alert(MESSAGES.sameData);
    return false;
  }

  return true;
}

// Lógica principal ao carregar a página
document.addEventListener("DOMContentLoaded", async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const id = urlParams.get("id"); // Obtém o ID da URL

  try {
    const data = await fetchRecordById(id);
    if (data.error) {
      alert(data.error);
      window.location.href = "/";
      return;
    }

    displayRecordDetails(data);
    setupDeleteButton(id);

    // Armazena os valores antigos para validação
    const oldValues = { name: data.name, email: data.email, CPF: data.CPF };

    // Lógica para atualizar o registro completo
    document
      .getElementById("update-form")
      .addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const record = Object.fromEntries(formData.entries());

        // Chama a rota PUT para atualizar completamente
        if (validateForm(record, oldValues)) {
          try {
            await updateRecord(record);
            alert(MESSAGES.updateSuccess);
            location.reload(); // Recarrega a página para refletir as mudanças
          } catch (error) {
            console.error("Erro ao atualizar registro:", error);
          }
        }
      });

    // Lógica para atualizar o registro parcialmente
    document
      .getElementById("update-partial-form")
      .addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const partialRecord = Object.fromEntries(formData.entries());

        // Carregue o registro atual antes de aplicar a atualização parcial
        const currentRecord = await fetchRecordById(partialRecord.id);

        // Atualiza apenas os campos que não estão vazios
        const updatedRecord = {
          ...currentRecord,
          ...Object.fromEntries(
            Object.entries(partialRecord).filter(([key, value]) => value !== "")
          ),
        };

        // Chama a rota PATCH para atualizar parcialmente
        try {
          await updatePartialRecord(updatedRecord);
          alert(MESSAGES.partialUpdateSuccess);
          location.reload(); // Recarrega a página para refletir as mudanças
        } catch (error) {
          console.error("Erro ao atualizar registro parcialmente:", error);
        }
      });
  } catch (error) {
    console.error("Erro ao buscar registro:", error);
  }
});
