// Importa o cliente MQTT e outras dependências
const mqtt = require("mqtt");
const {
  mqttHost, // Host do broker MQTT
  mqttTopic, // Tópico de temperatura
  heaterTopic, // Tópico do aquecedor
  heartbeatTopic, // Tópico de heartbeat
} = require("../config/mqttConfig");
const {
  connectToDb, // Função para conectar ao banco de dados
  storeTemperature, // Função para armazenar temperatura no banco
  updateHeaterStatus, // Função para atualizar o status do aquecedor
} = require("../database/database");
const fs = require("fs");
const { verify } = require("crypto");

// Carrega a chave pública usada para verificar assinaturas
const publicKey = fs.readFileSync("public_key.pem", "utf8");

// Variável para o cliente MQTT
let client;

// Função principal para inicializar o controlador
async function initializeController() {
  try {
    // Conecta ao banco de dados
    await connectToDb();
    console.log("Banco de dados conectado");

    // Conecta ao broker MQTT
    client = mqtt.connect(mqttHost);

    // Evento disparado quando o cliente conecta ao broker
    client.on("connect", () => {
      console.log("Controlador principal conectado ao broker MQTT");

      // Inscreve-se no tópico para receber mensagens de temperatura
      client.subscribe(mqttTopic, (err) => {
        if (err) {
          console.error(`Erro ao se inscrever no tópico ${mqttTopic}:`, err);
        }
      });
    });

    // Envia um "heartbeat" a cada 1 segundo para indicar que está ativo
    setInterval(() => {
      client.publish(heartbeatTopic, "alive");
    }, 1000);

    // Escuta mensagens recebidas no broker MQTT
    client.on("message", async (topic, message) => {
      if (topic === mqttTopic) {
        try {
          // Extrai os dados e a assinatura da mensagem
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

          // Garante que o valor da temperatura seja numérico
          parsedMessage.temperature = parseFloat(parsedMessage.temperature);

          // Validação básica de temperatura
          if (
            typeof parsedMessage.temperature !== "number" ||
            parsedMessage.temperature < -50 || // Temperatura mínima aceitável
            parsedMessage.temperature > 100 // Temperatura máxima aceitável
          ) {
            throw new Error("Valor de temperatura inválido recebido");
          }

          const { temperature } = parsedMessage;

          // Armazena a temperatura no banco de dados
          await storeTemperature(temperature);

          // Lógica para ligar/desligar o aquecedor com base na temperatura
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
  } catch (error) {
    console.error("Erro ao inicializar controlador principal", error);
    process.exit(1); // Encerra o processo em caso de erro grave
  }
}

// Inicializa o controlador principal ao carregar o script
initializeController();
