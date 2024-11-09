# O cliente utiliza o método rpyc.connect() para estabelecer uma conexão com o servidor. Após a conexão, o cliente chama 
# métodos remotos expostos pelo servidor para realizar as operações. A interação com o usuário é feita por meio de um menu 
# no terminal, e as opções do menu acionam os métodos correspondentes no servidor.


import rpyc


# Função para colorir o texto usando sequências de escape ANSI
def colorir_texto(texto, cor="default"):
    # Dicionário com cores e suas respectivas sequências ANSI
    cores = {
        "vermelho": "\033[91m",  # Cor vermelha
        "verde": "\033[92m",  # Cor verde
        "amarelo": "\033[93m",  # Cor amarela
        "azul": "\033[94m",  # Cor azul
        "magenta": "\033[95m",  # Cor magenta
        "ciano": "\033[96m",  # Cor ciano
        "negrito": "\033[1m",  # Cor negrito (intensificada)
        "default": "\033[0m",  # Reset para cor padrão
    }
    # Retorna o texto colorido com a cor solicitada, aplicando o reset no final
    return f"{cores.get(cor, cores['default'])}{texto}\033[0m"


# Conecta-se ao servidor utilizando a biblioteca rpyc
conn = rpyc.connect("localhost", 18861)  # Conexão com o servidor na porta 18861
proxy = conn.root  # Acessa o objeto root do servidor para chamar os métodos expostos


# Função para exibir o menu principal de opções para o usuário
def exibir_menu(status_na_sala):
    print(colorir_texto("\n" + "=" * 40, "azul"))  # Linha de separação superior
    if status_na_sala:  # Se o usuário está na sala, exibe o menu da sala
        print(
            colorir_texto(" Menu da Sala ".center(40, "="), "ciano")
        )  # Título centralizado
        # Opções disponíveis dentro da sala
        print(colorir_texto("1. Listar mensagens públicas", "negrito"))
        print(colorir_texto("2. Enviar mensagem pública", "negrito"))
        print(colorir_texto("3. Listar mensagens privadas", "negrito"))
        print(colorir_texto("4. Enviar mensagem privada", "negrito"))
        print(colorir_texto("5. Sair da sala", "negrito"))
        print(colorir_texto("6. Sair do sistema", "negrito"))
    else:  # Se o usuário não está na sala, exibe o menu de acesso
        print(colorir_texto(" Menu de Acesso ".center(40, "="), "ciano"))
        # Opções disponíveis fora da sala
        print(colorir_texto("1. Entrar na sala", "negrito"))
        print(colorir_texto("2. Listar usuários na sala", "negrito"))
        print(colorir_texto("3. Sair do sistema", "negrito"))
    print(colorir_texto("=" * 40, "azul"))  # Linha de separação inferior


# Função para interagir com o usuário e realizar as operações no sistema de chat
def interagir_com_usuario():
    print(colorir_texto("\nBem-vindo ao sistema de chat distribuído!", "magenta"))
    nome = input("Digite seu nome: ")  # Solicita o nome do usuário
    user_id = proxy.ingressar_no_sistema(nome)  # Registra o usuário no sistema
    print(
        colorir_texto(f"\n[SUCESSO] Você foi registrado com o ID: {user_id}", "verde")
    )  # Confirma o registro com o ID gerado

    # Loop principal para interagir com o sistema até que o usuário decida sair
    while True:
        status_na_sala = proxy.verificar_status_usuario(
            user_id
        )  # Verifica se o usuário está na sala
        exibir_menu(status_na_sala)  # Exibe o menu com base no status do usuário

        # Recebe e processa a opção escolhida pelo usuário
        opcao = input(colorir_texto("Escolha uma opção: ", "amarelo"))

        if not status_na_sala:  # Caso o usuário não esteja na sala
            # Opções para usuários fora da sala
            if opcao == "1":
                print(
                    colorir_texto(proxy.entrar_na_sala(user_id), "verde")
                )  # Entra na sala
            elif opcao == "2":
                usuarios = proxy.listar_usuarios()  # Lista os usuários na sala
                print(colorir_texto("\nUsuários na sala:\n\n", "ciano"))
                print(
                    colorir_texto(
                        ", ".join(usuarios) if usuarios else "Nenhum usuário na sala.",
                        "default",
                    )
                )
            elif opcao == "3":
                if user_id is not None:
                    proxy.remover_usuario(user_id)  # Remove o usuário do sistema
                    print(colorir_texto("Saindo do sistema... Até logo!", "magenta"))
                    break  # Encerra o programa
                else:
                    print(
                        colorir_texto(
                            "[ERRO] Usuário não encontrado ou já removido.", "vermelho"
                        )
                    )
                break  # Encerra o loop

            else:
                print(
                    colorir_texto("[ERRO] Opção inválida! Tente novamente.", "vermelho")
                )

        else:  # Caso o usuário esteja na sala
            # Opções para usuários dentro da sala
            if opcao == "1":
                mensagens = proxy.listar_mensagens()  # Lista as mensagens públicas
                print(colorir_texto("\nMensagens públicas:", "ciano"))
                if mensagens:
                    for msg in mensagens:
                        print(colorir_texto(f"- {msg}", "default"))
                else:
                    print(colorir_texto("Nenhuma mensagem pública ainda.", "default"))
            elif opcao == "2":
                mensagem = input(
                    "Digite a mensagem pública: "
                )  # Envia uma mensagem pública
                print(colorir_texto(proxy.enviar_mensagem(user_id, mensagem), "verde"))
            elif opcao == "3":
                mensagens_privadas = proxy.listar_mensagens_privadas(
                    user_id
                )  # Lista as mensagens privadas
                print(colorir_texto("\nMensagens privadas:", "ciano"))
                if mensagens_privadas:
                    for msg in mensagens_privadas:
                        print(colorir_texto(f"- {msg}", "default"))
                else:
                    print(colorir_texto("Nenhuma mensagem privada.", "default"))
            elif opcao == "4":
                try:
                    destinatario_id = int(
                        input("Digite o ID do destinatário: ")
                    )  # Solicita o ID do destinatário
                    mensagem = input(
                        "Digite a mensagem privada: "
                    )  # Envia uma mensagem privada
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
            elif opcao == "5":
                print(
                    colorir_texto(proxy.sair_da_sala(user_id), "amarelo")
                )  # Sai da sala
            elif opcao == "6":
                proxy.remover_usuario(user_id)  # Remove o usuário e sai do sistema
                print(colorir_texto("Saindo do sistema... Até logo!", "magenta"))
                break  # Encerra o programa
            else:
                print(
                    colorir_texto("[ERRO] Opção inválida! Tente novamente.", "vermelho")
                )


if __name__ == "__main__":
    interagir_com_usuario()  # Inicia a interação com o usuário
