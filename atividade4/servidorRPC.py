import rpyc
from rpyc.utils.server import ThreadedServer


def colorir_texto(texto, cor):
    cores = {
        "vermelho": "\033[91m",
        "verde": "\033[92m",
        "amarelo": "\033[93m",
        "azul": "\033[94m",
        "magenta": "\033[95m",
        "ciano": "\033[96m",
        "branco": "\033[97m",
        "reset": "\033[0m",
    }
    return f"{cores.get(cor, cores['reset'])}{texto}{cores['reset']}"


class ChatService(rpyc.Service):
    users = {}  # Armazena os usuários e suas identificações
    messages = []  # Armazena mensagens públicas
    private_messages = {}  # Armazena mensagens privadas (dicionário de destinatários)
    user_id_counter = 1  # Contador de IDs para garantir unicidade

    def exposed_ingressar_no_sistema(self, nome_usuario):
        user_id = ChatService.user_id_counter  # Use variável de classe
        ChatService.user_id_counter += 1  # Incrementa o contador para o próximo usuário
        ChatService.users[user_id] = {"nome": nome_usuario, "na_sala": False}
        print(
            colorir_texto(
                f"[LOG] Usuário '{nome_usuario}' entrou no sistema com ID {user_id}.",
                "verde",
            )
        )
        return user_id

    def exposed_entrar_na_sala(self, user_id):
        if user_id in ChatService.users:
            ChatService.users[user_id]["na_sala"] = True
            print(
                colorir_texto(
                    f"[LOG] Usuário '{ChatService.users[user_id]['nome']}' entrou na sala.",
                    "azul",
                )
            )
            return f"{ChatService.users[user_id]['nome']} entrou na sala."
        return colorir_texto("Usuário não encontrado.", "vermelho")

    def exposed_sair_da_sala(self, user_id):
        if user_id in ChatService.users and ChatService.users[user_id]["na_sala"]:
            ChatService.users[user_id]["na_sala"] = False
            print(
                colorir_texto(
                    f"[LOG] Usuário '{ChatService.users[user_id]['nome']}' saiu da sala.",
                    "amarelo",
                )
            )
            return f"{ChatService.users[user_id]['nome']} saiu da sala."
        return colorir_texto("Usuário não está na sala.", "vermelho")

    def exposed_enviar_mensagem(self, user_id, mensagem):
        if user_id in ChatService.users and ChatService.users[user_id]["na_sala"]:
            nome = ChatService.users[user_id]["nome"]
            ChatService.messages.append(f"{nome}: {mensagem}")
            print(
                colorir_texto(
                    f"[LOG] Mensagem pública de '{nome}': {mensagem}", "ciano"
                )
            )
            return "Mensagem enviada."
        return colorir_texto("Usuário não está na sala.", "vermelho")

    def exposed_listar_mensagens(self):
        return ChatService.messages

    def exposed_enviar_mensagem_usuario(self, user_id, destinatario_id, mensagem):
        if user_id in ChatService.users and destinatario_id in ChatService.users:
            if user_id != destinatario_id:
                remetente_nome = ChatService.users[user_id]["nome"]
                destinatario_nome = ChatService.users[destinatario_id]["nome"]
                msg = f"{remetente_nome} para {destinatario_nome}: {mensagem}"

                if destinatario_id not in ChatService.private_messages:
                    ChatService.private_messages[destinatario_id] = []
                ChatService.private_messages[destinatario_id].append(msg)

                if user_id not in ChatService.private_messages:
                    ChatService.private_messages[user_id] = []
                ChatService.private_messages[user_id].append(msg)

                print(
                    colorir_texto(
                        f"[LOG] Mensagem privada de '{remetente_nome}' para '{destinatario_nome}': {mensagem}",
                        "magenta",
                    )
                )
                return "Mensagem privada enviada."
            return colorir_texto(
                "Não é possível enviar mensagem para si mesmo.", "amarelo"
            )
        return colorir_texto("Usuário ou destinatário não encontrado.", "vermelho")

    def exposed_listar_usuarios(self):
        usuarios_ativos = [
            user_info["nome"]
            for user_info in ChatService.users.values()
            if user_info["na_sala"]
        ]
        return usuarios_ativos

    def exposed_listar_mensagens_privadas(self, user_id):
        return ChatService.private_messages.get(user_id, [])

    def exposed_remover_usuario(self, user_id):
        if user_id in self.users:
            nome_usuario = self.users[user_id]["nome"]
            del self.users[user_id]
            print(
                colorir_texto(
                    f"[LOG] Usuário '{nome_usuario}' removido do sistema.", "verde"
                )
            )
            return f"Usuário {nome_usuario} removido com sucesso."
        else:
            return colorir_texto(
                f"Erro: Usuário com ID {user_id} não encontrado.", "vermelho"
            )

    def exposed_verificar_status_usuario(self, user_id):
        # Retorna True se o usuário estiver na sala, False caso contrário
        if user_id in ChatService.users:
            return ChatService.users[user_id]["na_sala"]
        return False


if __name__ == "__main__":
    t = ThreadedServer(ChatService, port=18861)
    print(colorir_texto("[SERVIDOR INICIADO] Aguardando conexões...", "azul"))
    t.start()
