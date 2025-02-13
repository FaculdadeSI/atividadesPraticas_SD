// Endereço do broker MQTT (neste caso, local)
const mqttHost = "mqtt://localhost";

// Tópico para publicar ou subscrever informações de temperatura
const mqttTopic = "home/temperature";

// Tópico para controlar ou monitorar o aquecedor
const heaterTopic = "home/heater";

// Tópico para sinalizar o status do sistema (heartbeat)
const heartbeatTopic = "home/heartbeat";

// Exporta as constantes para serem usadas em outros módulos
module.exports = { mqttHost, mqttTopic, heaterTopic, heartbeatTopic };
