import rpyc

# Conexão com o servidor
proxy = rpyc.connect("localhost", 18861)

# Credenciamento no sistema
nome = input("Digite seu nome: ")
user_id = proxy.root.ingressar_no_sistema(nome)
print(f"Você foi registrado com o ID: {user_id}")

# Loop de interação com o sistema de mensagens
while True:
    print("\nEscolha uma opção:")
    print("1. Entrar na sala")
    print("2. Sair da sala")
    print("3. Enviar mensagem pública")
    print("4. Listar mensagens públicas")
    print("5. Enviar mensagem privada")
    print("6. Listar usuários na sala")
    print("7. Listar mensagens privadas")
    print("8. Sair")
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
        destinatario_id = int(input("Digite o ID do destinatário: "))
        mensagem = input("Digite sua mensagem privada: ")
        print(proxy.root.enviar_mensagem_usuario(user_id, destinatario_id, mensagem))

    elif escolha == "6":
        usuarios = proxy.root.listar_usuarios()
        print("\nUsuários na sala:")
        for usuario in usuarios:
            print(usuario)

    elif escolha == "7":
        mensagens_privadas = proxy.root.listar_mensagens_privadas(user_id)
        print("\nMensagens privadas:")
        for msg in mensagens_privadas:
            print(msg)

    elif escolha == "8":
        print("Saindo...")
        break
    else:
        print("Opção inválida. Tente novamente.")
