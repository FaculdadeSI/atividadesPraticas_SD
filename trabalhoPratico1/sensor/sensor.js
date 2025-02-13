const mqtt = require("mqtt"); // Biblioteca para comunicação via MQTT
const fs = require("fs"); // Biblioteca para manipulação de arquivos
const { sign } = require("crypto"); // Módulo para funções criptográficas
const { mqttHost, mqttTopic } = require("../config/mqttConfig"); // Configurações do MQTT

// Carrega a chave privada usada para assinar as mensagens
const privateKey = fs.readFileSync("private_key.pem", "utf8");

// Conecta ao broker MQTT com as configurações especificadas
const client = mqtt.connect(mqttHost);

client.on("connect", () => {
  console.log("Sensor conectado ao broker MQTT");

  // Envia mensagens de temperatura a cada 5 segundos
  setInterval(() => {
    const temperature = (Math.random() * 50 - 10).toFixed(2); // Gera um valor de temperatura entre -10°C e 40°C
    const message = JSON.stringify({
      temperature,
      timestamp: Date.now(), // Inclui o timestamp no payload
    });

    // Assina a mensagem com a chave privada para garantir autenticidade
    const signature = sign("sha256", Buffer.from(message), privateKey).toString(
      "base64" // Converte a assinatura para o formato Base64
    );

    // Publica a mensagem e sua assinatura no tópico especificado
    client.publish(mqttTopic, JSON.stringify({ message, signature }));
  }, 5000); // Intervalo de publicação: 5 segundos
});
