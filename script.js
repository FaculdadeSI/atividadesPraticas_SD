// Lógica para criar um novo registro
document
  .getElementById("create-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const record = Object.fromEntries(formData.entries());

    fetch("/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(record),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Erro ao criar registro."); // Adicionando verificação para erros
        }
        return response.json();
      })
      .then((data) => {
        console.log("Registro criado:", data);
        alert("Registro criado com sucesso!");
      })
      .catch((error) => console.error("Erro ao criar registro:", error));
  });

// Lógica para buscar registros pelo nome
document
  .getElementById("query-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const name = formData.get("name"); // Obter o nome

    fetch(`/queryByName?name=${encodeURIComponent(name)}`) // Chama a rota modificada
      .then((response) => {
        if (!response.ok) {
          throw new Error("Nenhum registro encontrado."); // Lança um erro se nenhum registro for encontrado
        }
        return response.json();
      })
      .then((data) => {
        // Aqui exibimos os registros encontrados
        const recordList = document.createElement("ul");
        data.forEach((record) => {
          const listItem = document.createElement("li");
          listItem.textContent = `${record.name} - ${record.email} - ${record.CPF}`;
          const selectButton = document.createElement("button");
          selectButton.textContent = "Selecionar";
          selectButton.onclick = () => {
            window.location.href = `record.html?id=${record.id}`; // Redireciona para a página de detalhes do registro
          };
          listItem.appendChild(selectButton);
          recordList.appendChild(listItem);
        });
        // Exibe a lista no DOM
        const container = document.querySelector(".container");
        container.appendChild(recordList);
      })
      .catch((error) => {
        alert(error.message);
        console.error("Erro ao buscar registros:", error);
      });
  });
