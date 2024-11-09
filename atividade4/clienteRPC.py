import rpyc

# Conecta ao servidor
conn = rpyc.connect("localhost", 18861)
proxy = conn.root


# Função para exibir o menu principal
def exibir_menu(status_na_sala):
    print("\n" + "=" * 40)
    if status_na_sala:
        print(" Menu da Sala ".center(40, "="))
        print("1. Listar mensagens públicas")
        print("2. Enviar mensagem pública")
        print("3. Enviar mensagem privada")
        print("4. Listar mensagens privadas")
        print("5. Sair da sala")
        print("6. Sair do sistema")
    else:
        print(" Menu de Acesso ".center(40, "="))
        print("1. Entrar na sala")
        print("2. Listar usuários na sala")
        print("3. Sair do sistema")
    print("=" * 40)


# Função para interagir com o usuário
def interagir_com_usuario():
    print("\nBem-vindo ao sistema de chat distribuído!")
    nome = input("Digite seu nome: ")
    user_id = proxy.ingressar_no_sistema(nome)
    print(f"\n[SUCESSO] Você foi registrado com o ID: {user_id}")

    while True:
        status_na_sala = proxy.verificar_status_usuario(user_id)
        exibir_menu(status_na_sala)

        # Receber e processar opção
        opcao = input("Escolha uma opção: ")

        if not status_na_sala:
            # Opções fora da sala
            if opcao == "1":
                print(proxy.entrar_na_sala(user_id))
            elif opcao == "2":
                usuarios = proxy.listar_usuarios()
                print("\nUsuários na sala:")
                print(", ".join(usuarios) if usuarios else "Nenhum usuário na sala.")
            elif opcao == "3":
                proxy.remover_usuario(user_id)
                print("Saindo do sistema... Até logo!")
                break
            else:
                print("[ERRO] Opção inválida! Tente novamente.")

        else:
            # Opções dentro da sala
            if opcao == "1":
                mensagens = proxy.listar_mensagens()
                print("\nMensagens públicas:")
                if mensagens:
                    for msg in mensagens:
                        print(f"- {msg}")
                else:
                    print("Nenhuma mensagem pública ainda.")
            elif opcao == "2":
                mensagem = input("Digite a mensagem pública: ")
                print(proxy.enviar_mensagem(user_id, mensagem))
            elif opcao == "3":
                try:
                    destinatario_id = int(input("Digite o ID do destinatário: "))
                    mensagem = input("Digite a mensagem privada: ")
                    print(
                        proxy.enviar_mensagem_usuario(
                            user_id, destinatario_id, mensagem
                        )
                    )
                except ValueError:
                    print("[ERRO] ID do destinatário deve ser um número.")
            elif opcao == "4":
                mensagens_privadas = proxy.listar_mensagens_privadas(user_id)
                print("\nMensagens privadas:")
                if mensagens_privadas:
                    for msg in mensagens_privadas:
                        print(f"- {msg}")
                else:
                    print("Nenhuma mensagem privada.")
            elif opcao == "5":
                print(proxy.sair_da_sala(user_id))
            elif opcao == "6":
                proxy.remover_usuario(user_id)
                print("Saindo do sistema... Até logo!")
                break
            else:
                print("[ERRO] Opção inválida! Tente novamente.")


if __name__ == "__main__":
    interagir_com_usuario()
