import rpyc
import time
import threading

# Conexão com o servidor
proxy = rpyc.connect("localhost", 18861)

# Credenciamento no sistema
nome = input("Digite seu nome: ")
user_id = proxy.root.ingressar_no_sistema(nome)
print(f"Você foi registrado com o ID: {user_id}")


# Função para verificar novas mensagens privadas
def verificar_mensagens_privadas():
    mensagens_vistas = set()  # Armazena mensagens já vistas para evitar duplicações
    while True:
        time.sleep(2)  # Verifica mensagens a cada 2 segundos
        mensagens_privadas = proxy.root.listar_mensagens_privadas(user_id)
        novas_mensagens = [
            msg for msg in mensagens_privadas if msg not in mensagens_vistas
        ]

        if novas_mensagens:
            print("\n[Novas Mensagens Privadas]:")
            for msg in novas_mensagens:
                print(msg)
                mensagens_vistas.add(msg)


# Inicia uma thread para monitorar as mensagens privadas
threading.Thread(target=verificar_mensagens_privadas, daemon=True).start()

# Loop de interação com o sistema de mensagens
while True:
    print("\nEscolha uma opção:")
    print("1. Entrar na sala")
    print("2. Sair da sala")
    print("3. Enviar mensagem pública")
    print("4. Listar mensagens públicas")
    print("5. Enviar mensagem privada")
    print("6. Listar usuários na sala")
    print("7. Sair")
    escolha = input("Digite o número da opção: ")

    if escolha == "1":
        print(proxy.root.entrar_na_sala(user_id))

    elif escolha == "2":
        print(proxy.root.sair_da_sala(user_id))

    elif escolha == "3":
        mensagem = input("Digite sua mensagem: ")
        print(proxy.root.enviar_mensagem(user_id, mensagem))

    elif escolha == "4":
        mensagens = proxy.root.listar_mensagens()
        print("\nMensagens públicas:")
        for msg in mensagens:
            print(msg)

    elif escolha == "5":
        try:
            destinatario_id = int(input("Digite o ID do destinatário: "))
            mensagem = input("Digite sua mensagem privada: ")
            print(
                proxy.root.enviar_mensagem_usuario(user_id, destinatario_id, mensagem)
            )
        except ValueError:
            print("ID do destinatário inválido.")

    elif escolha == "6":
        usuarios = proxy.root.listar_usuarios()
        print("\nUsuários na sala:")
        for usuario in usuarios:
            print(usuario)

    elif escolha == "7":
        print("Saindo...")
        break
    else:
        print("Opção inválida. Tente novamente.")
