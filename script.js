// Função para criar um novo registro
function createRecord(event) {
  event.preventDefault(); // Impede o envio padrão do formulário
  const formData = new FormData(event.target);
  const record = Object.fromEntries(formData.entries()); // Converte os dados do formulário em um objeto

  fetch("/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json", // Define o tipo de conteúdo
    },
    body: JSON.stringify(record), // Envia os dados como JSON
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Erro ao criar registro."); // Verifica se a resposta é OK
      }
      return response.json();
    })
    .then((data) => {
      console.log("Registro criado:", data); // Log no console do navegador
      alert("Registro criado com sucesso!"); // Alerta para o usuário
    })
    .catch((error) => console.error("Erro ao criar registro:", error)); // Log de erro no console
}

// Função para buscar registros pelo nome
function queryRecords(event) {
  event.preventDefault(); // Impede o envio padrão do formulário
  const formData = new FormData(event.target);
  const name = formData.get("name"); // Obtém o nome do formulário

  fetch(`/queryByName?name=${encodeURIComponent(name)}`) // Chama a rota para buscar registros
    .then((response) => {
      if (!response.ok) {
        throw new Error("Nenhum registro encontrado."); // Verifica se a resposta é OK
      }
      return response.json();
    })
    .then(displayRecords) // Chama a função para exibir os registros
    .catch((error) => {
      alert(error.message); // Alerta o usuário em caso de erro
      console.error("Erro ao buscar registros:", error); // Log de erro no console
    });
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
  container.appendChild(recordList);
}

// Adiciona os ouvintes de eventos aos formulários
document.getElementById("create-form").addEventListener("submit", createRecord);
document.getElementById("query-form").addEventListener("submit", queryRecords);
