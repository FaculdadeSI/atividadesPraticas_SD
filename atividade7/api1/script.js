const apiUrl = "http://127.0.0.1:5001";

function createTransaction() {
  // Captura os valores dos campos de transação no HTML
  const sender = document.getElementById("sender").value;
  const recipient = document.getElementById("recipient").value;
  const amount = document.getElementById("amount").value;

  // Envia a requisição POST para criar uma nova transação
  fetch(apiUrl + "/transactions/new", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sender, recipient, amount }), // Corpo da requisição com os dados da transação
  })
    .then((response) => response.json()) // Processa a resposta como JSON
    .then((data) => {
      console.log(data.message); // Exibe mensagem de sucesso ou erro no console
      mineBlock(); // Chama a função para minerar um bloco automaticamente após a transação
    });
}

function mineBlock() {
  // Envia a requisição GET para minerar um bloco
  fetch(apiUrl + "/mine")
    .then((response) => response.json()) // Processa a resposta como JSON
    .then((data) => {
      console.log("Bloco minerado:", data); // Exibe o bloco minerado no console
      resolveNodes(); // Chama a função para resolver conflitos de blockchain automaticamente
    });
}

function resolveNodes() {
  // Envia a requisição GET para resolver conflitos entre os nós
  fetch(apiUrl + "/nodes/resolve")
    .then((response) => response.json()) // Processa a resposta como JSON
    .then((data) => {
      console.log("Resolvendo conflitos:", data.message); // Exibe o status da resolução no console
      updateBlockchain(); // Atualiza a exibição da blockchain após resolver conflitos
    });
}

function updateBlockchain() {
  // Envia a requisição GET para obter a blockchain completa
  fetch(apiUrl + "/chain")
    .then((response) => response.json()) // Processa a resposta como JSON
    .then((data) => {
      // Exibe a blockchain formatada no elemento HTML com id "blockchain"
      document.getElementById("blockchain").textContent = JSON.stringify(
        data,
        null,
        2
      );
    });
}

// Atualiza a blockchain sempre que a página for carregada
updateBlockchain();
