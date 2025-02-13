// Importa dependências necessárias
const mqtt = require("mqtt");
const {
  mqttHost, // Host do broker MQTT
  mqttTopic, // Tópico de temperatura
  heaterTopic, // Tópico do aquecedor
  heartbeatTopic, // Tópico do heartbeat
} = require("../config/mqttConfig");
const {
  connectToDb, // Função para conectar ao banco de dados
  storeTemperature, // Função para armazenar temperatura no banco de dados
  updateHeaterStatus, // Função para atualizar o status do aquecedor
} = require("../database/database");
const fs = require("fs");
const { verify } = require("crypto");

// Carrega a chave pública para verificar assinaturas
const publicKey = fs.readFileSync("public_key.pem", "utf8");

// Variáveis globais para controlar o estado do sistema
let client; // Cliente MQTT para comunicação com o broker
let isMainControllerAlive = true; // Flag para indicar se o controlador principal está ativo
let mainControllerFailureTime = null; // Armazena o tempo de falha do controlador principal
let backupControllerStarted = false; // Flag para indicar se o controlador de backup foi iniciado

// Função para inicializar o controlador de backup
async function initializeBackupController() {
  if (backupControllerStarted) {
    return; // Evita reinicializar o controlador de backup
  }

  try {
    // Conecta ao banco de dados
    await connectToDb();
    console.log("Banco de dados conectado");

    // Conecta ao broker MQTT
    client = mqtt.connect(mqttHost);

    // Evento disparado ao conectar ao broker MQTT
    client.on("connect", () => {
      console.log("Backup controlador conectado ao broker MQTT");

      // Inscreve-se no tópico de temperatura
      client.subscribe(mqttTopic, (err) => {
        if (err) {
          console.error(`Erro ao se inscrever no tópico ${mqttTopic}:`, err);
        }
      });
    });

    // Processa mensagens recebidas no tópico de temperatura
    client.on("message", async (topic, message) => {
      // Só processa mensagens se o controlador principal estiver inativo
      if (topic === mqttTopic && !isMainControllerAlive) {
        try {
          const { message: data, signature } = JSON.parse(message.toString());

          // Verifica a assinatura para garantir a integridade dos dados
          const isValid = verify(
            "sha256",
            Buffer.from(data),
            publicKey,
            Buffer.from(signature, "base64")
          );

          if (!isValid) {
            throw new Error("Assinatura inválida. Dados comprometidos.");
          }

          // Faz o parsing dos dados para obter o payload
          const parsedMessage = JSON.parse(data);

          // Converte a temperatura para número e valida o intervalo esperado
          parsedMessage.temperature = parseFloat(parsedMessage.temperature);

          if (
            typeof parsedMessage.temperature !== "number" ||
            parsedMessage.temperature < -9 || // Temperatura mínima aceitável
            parsedMessage.temperature > 41 // Temperatura máxima aceitável
          ) {
            throw new Error("Valor de temperatura inválido recebido");
          }

          const { temperature } = parsedMessage;

          // Armazena a temperatura no banco de dados
          await storeTemperature(temperature);

          // Decide ligar ou desligar o aquecedor com base na temperatura
          if (temperature < 15) {
            await updateHeaterStatus("on");
            client.publish(heaterTopic, "on");
          } else if (temperature >= 22) {
            await updateHeaterStatus("off");
            client.publish(heaterTopic, "off");
          }
        } catch (error) {
          console.error("Erro ao processar mensagem MQTT:", error);
        }
      }
    });

    backupControllerStarted = true; // Marca o controlador de backup como iniciado
  } catch (error) {
    console.error("Erro ao inicializar controlador de backup", error);
    process.exit(1); // Encerra o processo em caso de erro grave
  }
}

// Função para monitorar a saúde do controlador principal
function checkMainControllerHealth() {
  // Para de verificar o controlador principal se o backup já foi iniciado
  if (backupControllerStarted) {
    console.log(
      "Backup controlador iniciado. Verificação do principal interrompida."
    );
    return;
  }

  // Conecta ao broker MQTT para monitorar o heartbeat
  const heartbeatClient = mqtt.connect(mqttHost);

  heartbeatClient.on("connect", () => {
    console.log("Backup controlador monitorando o heartbeat do principal");

    // Inscreve-se no tópico de heartbeat
    heartbeatClient.subscribe(heartbeatTopic, (err) => {
      if (err) {
        console.error(`Erro ao se inscrever no tópico ${heartbeatTopic}:`, err);
      }
    });
  });

  // Processa mensagens do tópico de heartbeat
  heartbeatClient.on("message", (topic, message) => {
    if (topic === heartbeatTopic) {
      if (message.toString() === "alive") {
        isMainControllerAlive = true; // Controlador principal está ativo
        mainControllerFailureTime = null; // Reseta o tempo de falha
      }
    }
  });

  // Intervalo regular para verificar a saúde do controlador principal
  setInterval(() => {
    if (!isMainControllerAlive) {
      // Se o principal falhou por mais de 1 segundo, inicializa o backup
      if (!mainControllerFailureTime) {
        mainControllerFailureTime = Date.now();
      } else if (Date.now() - mainControllerFailureTime > 1000) {
        initializeBackupController(); // Inicializa o controlador de backup
      }
    } else {
      isMainControllerAlive = false; // Reseta a flag após cada intervalo
    }
  }, 1000); // Verifica a cada 1 segundo
}

// Inicia a verificação de saúde do controlador principal
checkMainControllerHealth();
