// Constantes para URLs e mensagens
const API_URLS = {
  create: "/create",
  queryByName: "/queryByName",
};

const MESSAGES = {
  createSuccess: "Registro criado com sucesso!",
  createError: "Erro ao criar registro.",
  queryError: "Nenhum registro encontrado.",
};

// Função para criar um novo registro
async function createRecord(event) {
  event.preventDefault(); // Impede o envio padrão do formulário

  const formData = new FormData(event.target);
  const record = Object.fromEntries(formData.entries()); // Converte os dados do formulário em um objeto

  try {
    const response = await fetch(API_URLS.create, {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // Define o tipo de conteúdo
      },
      body: JSON.stringify(record), // Envia os dados como JSON
    });

    if (!response.ok) {
      throw new Error(MESSAGES.createError); // Verifica se a resposta é OK
    }

    const data = await response.json();
    alert(MESSAGES.createSuccess); // Alerta para o usuário
  } catch (error) {
    console.error("Erro ao criar registro:", error);
  }
}

// Função para buscar registros pelo nome
async function queryRecords(event) {
  event.preventDefault(); // Impede o envio padrão do formulário

  const formData = new FormData(event.target);
  const name = formData.get("name"); // Obtém o nome do formulário

  try {
    const response = await fetch(
      `${API_URLS.queryByName}?name=${encodeURIComponent(name)}`
    ); // Chama a rota para buscar registros

    if (!response.ok) {
      throw new Error(MESSAGES.queryError); // Verifica se a resposta é OK
    }

    const data = await response.json();
    displayRecords(data); // Chama a função para exibir os registros
  } catch (error) {
    alert(error.message); // Alerta o usuário em caso de erro
    console.error("Erro ao buscar registros:", error);
  }
}

// Função para exibir os registros encontrados
function displayRecords(data) {
  const recordList = document.createElement("ul"); // Cria uma lista para os registros

  data.forEach((record) => {
    const listItem = document.createElement("li");
    listItem.textContent = `${record.name} - ${record.email} - ${record.CPF}`; // Adiciona informações do registro

    // Cria um botão para selecionar o registro
    const selectButton = document.createElement("button");
    selectButton.textContent = "Selecionar";
    selectButton.onclick = () => {
      window.location.href = `record.html?id=${record.id}`; // Redireciona para a página de detalhes do registro
    };

    listItem.appendChild(selectButton); // Adiciona o botão ao item da lista
    recordList.appendChild(listItem); // Adiciona o item da lista ao elemento UL
  });

  // Exibe a lista de registros no DOM
  const container = document.querySelector(".container");
  container.innerHTML = ""; // Limpa registros anteriores
  container.appendChild(recordList); // Adiciona a nova lista ao DOM
}

// Adiciona os ouvintes de eventos aos formulários
document.getElementById("create-form").addEventListener("submit", createRecord);
document.getElementById("query-form").addEventListener("submit", queryRecords);
