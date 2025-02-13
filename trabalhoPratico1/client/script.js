// Função para obter o status do aquecedor
async function getHeaterStatus() {
  try {
    const response = await fetch("http://localhost:3000/heater-status"); // Faz a requisição para obter o status
    const data = await response.json(); // Converte a resposta para formato JSON
    let statusText = "Desconhecido"; // Valor padrão do status
    let heaterEmoji = "🔴"; // Emoji padrão para aquecedor desligado

    if (data.status) {
      if (data.status === "on") {
        statusText = "Ligado"; // Se aquecedor estiver ligado
        heaterEmoji = "🟢"; // Emoji para aquecedor ligado
      } else {
        statusText = "Desligado"; // Se aquecedor estiver desligado
        heaterEmoji = "🔴"; // Emoji para aquecedor desligado
      }
    }

    // Atualiza o texto do status do aquecedor com o emoji correspondente
    document.getElementById(
      "heater-status"
    ).innerText = `${statusText} ${heaterEmoji}`;
  } catch (error) {
    console.error("Erro ao obter o status do aquecedor", error); // Captura erros caso a requisição falhe
  }
}

// Função para obter a temperatura
async function getTemperature() {
  try {
    const response = await fetch("http://localhost:3000/temperature"); // Faz a requisição para obter a temperatura
    const data = await response.json(); // Converte a resposta para formato JSON
    let temperatureText = "--"; // Valor padrão para temperatura
    let temperatureEmoji = "❄️"; // Emoji padrão para floco de neve (temperaturas abaixo de 18)

    if (data.temperature !== null) {
      const temperature = parseFloat(data.temperature); // Converte a temperatura para número de ponto flutuante

      // Verifica em que faixa de temperatura o valor se encaixa
      if (temperature >= 22) {
        temperatureText = `${temperature.toFixed(2)}ºC`; // Temperatura alta (acima de 22°C)
        temperatureEmoji = "☀️"; // Emoji para temperatura quente (sol)
      } else if (temperature < 18) {
        temperatureText = `${temperature.toFixed(2)}ºC`; // Temperatura fria (abaixo de 18°C)
        temperatureEmoji = "❄️"; // Emoji para temperatura muito fria (neve)
      } else {
        temperatureText = `${temperature.toFixed(2)}ºC`; // Temperatura amena (entre 18°C e 22°C)
        temperatureEmoji = "🌤️"; // Emoji para temperatura amena (sol e nuvem)
      }
    }

    // Atualiza o texto da temperatura com o emoji correspondente
    document.getElementById(
      "temperature"
    ).innerText = `${temperatureText} ${temperatureEmoji}`;
  } catch (error) {
    console.error("Erro ao obter a temperatura", error); // Captura erros caso a requisição falhe
  }
}

// Função para enviar um comando para controlar o aquecedor
async function sendCommand(command) {
  try {
    const response = await fetch("http://localhost:3000/heater-command", {
      method: "POST", // Envia a requisição POST
      headers: { "Content-Type": "application/json" }, // Define o tipo de conteúdo como JSON
      body: JSON.stringify({ command }), // Envia o comando em formato JSON
    });
    const data = await response.json(); // Converte a resposta para formato JSON
    // Atualiza o status após enviar o comando
    getHeaterStatus();
  } catch (error) {
    console.error("Erro ao enviar o comando", error); // Captura erros caso a requisição falhe
  }
}

// Função para alternar o estado do aquecedor (ligar/desligar)
async function toggleHeater() {
  try {
    // Obtém o status atual do aquecedor
    const response = await fetch("http://localhost:3000/heater-status");
    const data = await response.json();

    // Determina o novo comando baseado no status atual
    const newCommand = data.status === "on" ? "off" : "on";

    // Envia o novo comando para alternar o estado
    await sendCommand(newCommand);

    // Atualiza a interface com o novo status
    await getHeaterStatus();
  } catch (error) {
    console.error("Erro ao alternar o aquecedor", error); // Captura erros caso a requisição falhe
  }
}

// Função para atualizar o botão de controle do aquecedor
async function updateToggleButton() {
  try {
    const response = await fetch("http://localhost:3000/heater-status"); // Faz a requisição para obter o status atual
    const data = await response.json();
    const button = document.getElementById("toggle-heater"); // Obtém o botão de controle

    // Atualiza o texto e estilo do botão baseado no status do aquecedor
    if (data.status === "on") {
      button.innerText = "Desligar Aquecedor"; // Se aquecedor estiver ligado
      button.style.background = "linear-gradient(45deg, #f44336, #d32f2f)"; // Estilo do botão (vermelho)
    } else {
      button.innerText = "Ligar Aquecedor"; // Se aquecedor estiver desligado
      button.style.background = "linear-gradient(45deg, #4caf50, #45a049)"; // Estilo do botão (verde)
    }
  } catch (error) {
    console.error("Erro ao atualizar botão de alternância", error); // Captura erros caso a requisição falhe
  }
}

// Função para inicializar os dados da página
async function initializePage() {
  await getHeaterStatus(); // Obtém o status inicial do aquecedor
  await getTemperature(); // Obtém a temperatura inicial
}

// Atualiza a interface regularmente
setInterval(() => {
  getHeaterStatus(); // Atualiza o status do aquecedor
  getTemperature(); // Atualiza a temperatura
  updateToggleButton(); // Atualiza o botão de controle
}, 100);

// Inicializa a página assim que a janela for carregada
window.onload = async function () {
  await initializePage(); // Inicializa os dados da página
  await updateToggleButton(); // Atualiza o botão de controle
};
