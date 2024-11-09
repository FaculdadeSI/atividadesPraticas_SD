import rpyc

# Conecta ao servidor
conn = rpyc.connect("localhost", 18861)
proxy = conn.root


# Função para interagir com o usuário
def interagir_com_usuario():
    nome = input("Digite seu nome: ")
    user_id = proxy.ingressar_no_sistema(nome)
    print(f"Você foi registrado com o ID: {user_id}")

    # Lógica de opções do menu
    while True:
        if not proxy.verificar_status_usuario(user_id):
            # Se o usuário não estiver na sala, só pode entrar ou listar integrantes
            print("\nEscolha uma opção:")
            print("1. Entrar na sala")
            print("2. Listar usuários na sala")
            print("3. Sair")
            opcao = input("Digite o número da opção: ")

            if opcao == "1":
                print(proxy.entrar_na_sala(user_id))
            elif opcao == "2":
                usuarios = proxy.listar_usuarios()
                print(
                    "Usuários na sala:",
                    ", ".join(usuarios) if usuarios else "Nenhum usuário na sala.",
                )
            elif opcao == "3":
                proxy.remover_usuario(user_id)  # Remove o usuário do servidor
                print("Saindo...")
                break
            else:
                print("Opção inválida! Tente novamente.")
        else:
            # Se o usuário estiver na sala, pode acessar todas as opções
            print("\nEscolha uma opção:")
            print("1. Listar mensagens públicas")
            print("2. Enviar mensagem pública")
            print("3. Enviar mensagem privada")
            print("4. Listar mensagens privadas")
            print("5. Sair da sala")
            print("6. Sair")
            opcao = input("Digite o número da opção: ")

            if opcao == "1":
                mensagens = proxy.listar_mensagens()
                print("Mensagens públicas:")
                if mensagens:
                    for msg in mensagens:
                        print(msg)
                else:
                    print("Nenhuma mensagem pública ainda.")
            elif opcao == "2":
                mensagem = input("Digite a mensagem para enviar: ")
                print(proxy.enviar_mensagem(user_id, mensagem))
            elif opcao == "3":
                destinatario_id = int(input("Digite o ID do destinatário: "))
                mensagem = input("Digite a mensagem privada: ")
                print(proxy.enviar_mensagem_usuario(user_id, destinatario_id, mensagem))
            elif opcao == "4":
                mensagens_privadas = proxy.listar_mensagens_privadas(user_id)
                print("Mensagens privadas:")
                if mensagens_privadas:
                    for msg in mensagens_privadas:
                        print(msg)
                else:
                    print("Nenhuma mensagem privada.")
            elif opcao == "5":
                print(proxy.sair_da_sala(user_id))
            elif opcao == "6":
                proxy.remover_usuario(user_id)  # Remove o usuário do servidor
                print("Saindo...")
                break
            else:
                print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    interagir_com_usuario()
