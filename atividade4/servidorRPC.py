import rpyc


class ChatService(rpyc.Service):
    def __init__(self):
        self.users = {}  # Armazena os usuários e suas identificações
        self.messages = []  # Armazena mensagens públicas
        self.private_messages = (
            {}
        )  # Armazena mensagens privadas (dicionário de destinatários)

    def exposed_ingressar_no_sistema(self, nome_usuario):
        # Atribui um ID único para o novo usuário
        user_id = len(self.users) + 1
        self.users[user_id] = {"nome": nome_usuario, "na_sala": False}
        return user_id

    def exposed_entrar_na_sala(self, user_id):
        # Permite ao usuário ingressar na sala de bate-papo
        if user_id in self.users:
            self.users[user_id]["na_sala"] = True
            return f"{self.users[user_id]['nome']} entrou na sala."
        return "Usuário não encontrado."

    def exposed_sair_da_sala(self, user_id):
        # Permite ao usuário sair da sala de bate-papo
        if user_id in self.users and self.users[user_id]["na_sala"]:
            self.users[user_id]["na_sala"] = False
            return f"{self.users[user_id]['nome']} saiu da sala."
        return "Usuário não está na sala."

    def exposed_enviar_mensagem(self, user_id, mensagem):
        # Armazena a mensagem no histórico de mensagens públicas
        if user_id in self.users and self.users[user_id]["na_sala"]:
            nome = self.users[user_id]["nome"]
            self.messages.append(f"{nome}: {mensagem}")
            return "Mensagem enviada."
        return "Usuário não está na sala."

    def exposed_listar_mensagens(self):
        # Retorna a lista de todas as mensagens públicas
        return self.messages

    def exposed_enviar_mensagem_usuario(self, user_id, destinatario_id, mensagem):
        # Envia uma mensagem privada para outro usuário
        if user_id in self.users and destinatario_id in self.users:
            if user_id != destinatario_id:
                remetente_nome = self.users[user_id]["nome"]
                destinatario_nome = self.users[destinatario_id]["nome"]
                msg = f"{remetente_nome} para {destinatario_nome}: {mensagem}"

                # Adiciona a mensagem no histórico de mensagens privadas
                if destinatario_id not in self.private_messages:
                    self.private_messages[destinatario_id] = []
                self.private_messages[destinatario_id].append(msg)

                if user_id not in self.private_messages:
                    self.private_messages[user_id] = []
                self.private_messages[user_id].append(msg)

                return "Mensagem privada enviada."
            return "Não é possível enviar mensagem para si mesmo."
        return "Usuário ou destinatário não encontrado."

    def exposed_listar_usuarios(self):
        # Lista todos os usuários ativos na sala
        usuarios_ativos = [
            user_info["nome"]
            for user_info in self.users.values()
            if user_info["na_sala"]
        ]
        return usuarios_ativos

    def exposed_listar_mensagens_privadas(self, user_id):
        # Retorna a lista de todas as mensagens privadas para o usuário
        return self.private_messages.get(user_id, [])


from rpyc.utils.server import ThreadedServer

t = ThreadedServer(ChatService, port=18861)
t.start()
