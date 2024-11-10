# Este código configura um cliente MQTT que se conecta ao broker, assina um tópico e recebe atualizações de movimento de outros jogadores.
# Mensagens são adicionadas a uma fila para processamento.

import paho.mqtt.client as mqtt
import json


class MQTTSubscriber:
    def __init__(self, broker, port, topic, player_id, message_queue):
        # Inicializa o cliente MQTT e armazena as configurações de conexão
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.topic = topic
        self.player_id = player_id  # ID do jogador local
        self.message_queue = message_queue  # Referência para a fila de mensagens

        # Define o callback para processar mensagens recebidas
        self.client.on_message = self.on_message
        # Conecta ao broker MQTT
        self.client.connect(broker, port)
        # Assina o tópico para receber mensagens
        self.client.subscribe(topic)

    # Função executada quando uma mensagem é recebida
    def on_message(self, client, userdata, msg):
        message = json.loads(msg.payload.decode())
        if (
            message["player_id"] != self.player_id
        ):  # Ignora mensagens do próprio jogador
            print(f"Movimento recebido: {message}")
            self.message_queue.put(message)  # Adiciona a mensagem à fila

    # Mantém o assinante em execução
    def start(self):
        self.client.loop_forever()
