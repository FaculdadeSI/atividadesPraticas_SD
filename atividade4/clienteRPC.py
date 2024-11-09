import rpyc


# Sequências de escape ANSI para cores
def colorir_texto(texto, cor="default"):
    cores = {
        "vermelho": "\033[91m",
        "verde": "\033[92m",
        "amarelo": "\033[93m",
        "azul": "\033[94m",
        "magenta": "\033[95m",
        "ciano": "\033[96m",
        "negrito": "\033[1m",
        "default": "\033[0m",
    }
    return f"{cores.get(cor, cores['default'])}{texto}\033[0m"


# Conecta ao servidor
conn = rpyc.connect("localhost", 18861)
proxy = conn.root


# Função para exibir o menu principal
def exibir_menu(status_na_sala):
    print(colorir_texto("\n" + "=" * 40, "azul"))
    if status_na_sala:
        print(colorir_texto(" Menu da Sala ".center(40, "="), "ciano"))
        print(colorir_texto("1. Listar mensagens públicas", "negrito"))
        print(colorir_texto("2. Enviar mensagem pública", "negrito"))
        print(colorir_texto("3. Enviar mensagem privada", "negrito"))
        print(colorir_texto("4. Listar mensagens privadas", "negrito"))
        print(colorir_texto("5. Sair da sala", "negrito"))
        print(colorir_texto("6. Sair do sistema", "negrito"))
    else:
        print(colorir_texto(" Menu de Acesso ".center(40, "="), "ciano"))
        print(colorir_texto("1. Entrar na sala", "negrito"))
        print(colorir_texto("2. Listar usuários na sala", "negrito"))
        print(colorir_texto("3. Sair do sistema", "negrito"))
    print(colorir_texto("=" * 40, "azul"))


# Função para interagir com o usuário
def interagir_com_usuario():
    print(colorir_texto("\nBem-vindo ao sistema de chat distribuído!", "magenta"))
    nome = input("Digite seu nome: ")
    user_id = proxy.ingressar_no_sistema(nome)
    print(
        colorir_texto(f"\n[SUCESSO] Você foi registrado com o ID: {user_id}", "verde")
    )

    while True:
        status_na_sala = proxy.verificar_status_usuario(user_id)
        exibir_menu(status_na_sala)

        # Receber e processar opção
        opcao = input(colorir_texto("Escolha uma opção: ", "amarelo"))

        if not status_na_sala:
            # Opções fora da sala
            if opcao == "1":
                print(colorir_texto(proxy.entrar_na_sala(user_id), "verde"))
            elif opcao == "2":
                usuarios = proxy.listar_usuarios()
                print(colorir_texto("\nUsuários na sala:", "ciano"))
                print(
                    colorir_texto(
                        ", ".join(usuarios) if usuarios else "Nenhum usuário na sala.",
                        "default",
                    )
                )
            elif opcao == "3":
                proxy.remover_usuario(user_id)
                print(colorir_texto("Saindo do sistema... Até logo!", "magenta"))
                break
            else:
                print(
                    colorir_texto("[ERRO] Opção inválida! Tente novamente.", "vermelho")
                )

        else:
            # Opções dentro da sala
            if opcao == "1":
                mensagens = proxy.listar_mensagens()
                print(colorir_texto("\nMensagens públicas:", "ciano"))
                if mensagens:
                    for msg in mensagens:
                        print(colorir_texto(f"- {msg}", "default"))
                else:
                    print(colorir_texto("Nenhuma mensagem pública ainda.", "default"))
            elif opcao == "2":
                mensagem = input("Digite a mensagem pública: ")
                print(colorir_texto(proxy.enviar_mensagem(user_id, mensagem), "verde"))
            elif opcao == "3":
                try:
                    destinatario_id = int(input("Digite o ID do destinatário: "))
                    mensagem = input("Digite a mensagem privada: ")
                    print(
                        colorir_texto(
                            proxy.enviar_mensagem_usuario(
                                user_id, destinatario_id, mensagem
                            ),
                            "verde",
                        )
                    )
                except ValueError:
                    print(
                        colorir_texto(
                            "[ERRO] ID do destinatário deve ser um número.", "vermelho"
                        )
                    )
            elif opcao == "4":
                mensagens_privadas = proxy.listar_mensagens_privadas(user_id)
                print(colorir_texto("\nMensagens privadas:", "ciano"))
                if mensagens_privadas:
                    for msg in mensagens_privadas:
                        print(colorir_texto(f"- {msg}", "default"))
                else:
                    print(colorir_texto("Nenhuma mensagem privada.", "default"))
            elif opcao == "5":
                print(colorir_texto(proxy.sair_da_sala(user_id), "amarelo"))
            elif opcao == "6":
                proxy.remover_usuario(user_id)
                print(colorir_texto("Saindo do sistema... Até logo!", "magenta"))
                break
            else:
                print(
                    colorir_texto("[ERRO] Opção inválida! Tente novamente.", "vermelho")
                )


if __name__ == "__main__":
    interagir_com_usuario()
