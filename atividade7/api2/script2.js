const apiUrl = "http://127.0.0.1:5002"; // Mude para a URL correta da API

function createTransaction() {
  const sender = document.getElementById("sender").value;
  const recipient = document.getElementById("recipient").value;
  const amount = document.getElementById("amount").value;

  fetch(apiUrl + "/transactions/new", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sender, recipient, amount }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data.message);
      mineBlock(); // Minera automaticamente após criar a transação
    });
}

function mineBlock() {
  fetch(apiUrl + "/mine")
    .then((response) => response.json())
    .then((data) => {
      console.log("Bloco minerado:", data);
      resolveNodes(); // Após minerar, resolve conflitos automaticamente
    });
}

function resolveNodes() {
  fetch(apiUrl + "/nodes/resolve")
    .then((response) => response.json())
    .then((data) => {
      console.log("Resolvendo conflitos:", data.message);
      updateBlockchain(); // Após resolver, atualiza a exibição da blockchain
    });
}

function updateBlockchain() {
  fetch(apiUrl + "/chain")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("blockchain").textContent = JSON.stringify(
        data,
        null,
        2
      );
    });
}

// Atualiza ao carregar a página
updateBlockchain();
