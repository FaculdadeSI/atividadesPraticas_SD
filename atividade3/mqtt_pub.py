# Este código configura um cliente MQTT para publicar mensagens em um tópico específico (`self.topic`), enviando as
# informações de posição e movimento do jogador.

import json
import paho.mqtt.client as mqtt


class MQTTPublisher:

    def __init__(self, broker, port, topic):
        # Inicializa o cliente MQTT e conecta ao broker
        self.client = mqtt.Client()
        self.client.connect(broker, port)
        self.topic = topic  # Tópico no qual as mensagens serão publicadas

    def publish(self, player_id, x, y, direction, color, time):
        # Cria a mensagem com informações do jogador
        message = {
            "player_id": player_id,
            "x": x,
            "y": y,
            "direction": direction,
            "color": color,
            "time": time,
        }
        # Publica a mensagem JSON no tópico especificado
        self.client.publish(self.topic, json.dumps(message))
