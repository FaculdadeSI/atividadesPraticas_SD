# O código usa MQTT para comunicação em rede. O jogador publica sua posição no tópico `game/move`, e outros jogadores
# assinam esse tópico para receber atualizações em tempo real, permitindo sincronização de movimentos.

from queue import Queue
import turtle
import time
import random
import mqtt_pub  # Importa módulo para publicar mensagens via MQTT
import mqtt_sub  # Importa módulo para assinar e receber mensagens via MQTT
import threading

delay = 0.01  # Delay para controle de atualização

# Pontuação
score = 0
high_score = 0

# Configura a tela do jogo
wn = turtle.Screen()
wn.title("Move Game by Gaby and Mariana")
wn.bgcolor("gray")
wn.setup(width=600, height=600)
wn.tracer(0)  # Desativa atualizações automáticas da tela

players = {}  # Dicionário para armazenar jogadores
last_position = (0, 0)  # Posição anterior para verificar mudanças
message_queue = Queue()  # Fila para mensagens recebidas


# Função para criar um jogador (bola)
def create_player(color):
    player = turtle.Turtle()
    player.speed(0)
    player.shape("circle")
    player.color(color)
    player.penup()
    player.id = random.randint(1000, 9999)  # Gera um ID único
    player.time = time.time()
    player.goto(0, 0)
    player.direction = "stop"
    return player


# Função para criar texto exibido na tela
def create_text():
    text = turtle.Turtle()
    text.color("black")
    text.penup()
    text.hideturtle()
    return text


# Jogador principal configurado com cor aleatória
head_color = random.choice(
    ["red", "blue", "green", "yellow", "purple", "black", "pink", "orange"]
)
head = create_player(head_color)
text = create_text()


# Atualiza a posição dos jogadores conforme a mensagem recebida
def update_players(message):
    global last_position
    print(f"Update player: {message}")
    player_id = message["player_id"]
    print(f"Players: {players}")
    if player_id in players:
        # Atualiza jogador existente se a posição mudou
        if (message["x"], message["y"]) != last_position:
            last_position = (message["x"], message["y"])
            players[player_id].goto(message["x"], message["y"])
    else:
        # Adiciona novo jogador
        players[player_id] = create_player(message["color"])
        players[player_id].goto(message["x"], message["y"])
        players[player_id].showturtle()


# Funções de controle de movimento
def go_up():
    head.direction = "up"


def go_down():
    head.direction = "down"


def go_left():
    head.direction = "left"


def go_right():
    head.direction = "right"


def stop():
    head.direction = "stop"


def close():
    wn.bye()


# Movimenta o jogador e publica a nova posição
def move(pub):
    move_time = time.time()
    head.time = move_time

    text.clear()
    text.goto(head.xcor(), head.ycor() + 10)  # Exibe ID acima da bola
    text.write(head.id, align="center", font=("Arial", 12, "normal"))

    # Movimentos conforme direção
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 2)
        pub.publish(
            head.id,
            head.xcor(),
            head.ycor(),
            head.direction,
            head.color()[0],
            move_time,
        )

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 2)
        pub.publish(
            head.id,
            head.xcor(),
            head.ycor(),
            head.direction,
            head.color()[0],
            move_time,
        )

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 2)
        pub.publish(
            head.id,
            head.xcor(),
            head.ycor(),
            head.direction,
            head.color()[0],
            move_time,
        )

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 2)
        pub.publish(
            head.id,
            head.xcor(),
            head.ycor(),
            head.direction,
            head.color()[0],
            move_time,
        )


# Teclas de controle
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(close, "Escape")
wn.onkeypress(stop, "Return")


# Função principal
def main():
    broker = "localhost"  # Endereço do broker MQTT
    port = 1883  # Porta para MQTT
    topic = "game/move"

    global head
    actual_player_id = head.id

    # Configura publicador e assinante MQTT
    pub = mqtt_pub.MQTTPublisher(broker, port, topic)
    sub = mqtt_sub.MQTTSubscriber(broker, port, topic, actual_player_id, message_queue)

    # Inicia o assinante em uma nova thread
    sub_thread = threading.Thread(target=sub.start)
    sub_thread.start()

    while True:
        wn.update()
        move(pub)
        # Verifica mensagens na fila e atualiza jogadores
        if not message_queue.empty():
            message = message_queue.get()
            update_players(message)

        time.sleep(delay)


if __name__ == "__main__":
    main()
