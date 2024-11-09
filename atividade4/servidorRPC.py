# Utiliza a biblioteca rpyc para fornecer um serviço distribuído RPC (Remote Procedure Call). O RPC permite que os métodos 
# expostos pelo servidor sejam chamados remotamente, como se estivessem sendo executados localmente. A classe ChatService 
# expõe diversos métodos que podem ser acessados remotamente pelos clientes. O servidor usa o ThreadedServer da biblioteca 
# rpyc para aceitar múltiplas conexões simultâneas, permitindo a comunicação entre os usuários de maneira distribuída.



import rpyc
from rpyc.utils.server import ThreadedServer


# Função para colorir o texto no terminal, conforme a cor especificada
def colorir_texto(texto, cor):
    cores = {
        "vermelho": "\033[91m",  # Vermelho para erros
        "verde": "\033[92m",  # Verde para mensagens de sucesso
        "amarelo": "\033[93m",  # Amarelo para alertas
        "azul": "\033[94m",  # Azul para informações gerais
        "magenta": "\033[95m",  # Magenta para mensagens privadas
        "ciano": "\033[96m",  # Ciano para mensagens públicas
        "branco": "\033[97m",  # Branco para texto normal
        "reset": "\033[0m",  # Reset para voltar à cor padrão
    }
    return f"{cores.get(cor, cores['reset'])}{texto}{cores['reset']}"


# Classe que implementa os serviços do chat
class ChatService(rpyc.Service):
    # Armazena os usuários e suas identificações
    users = {}
    # Lista para armazenar mensagens públicas
    messages = []
    # Dicionário para mensagens privadas
    private_messages = {}
    # Contador para gerar IDs únicos de usuários
    user_id_counter = 1

    # Método para o usuário ingressar no sistema e obter um ID
    def exposed_ingressar_no_sistema(self, nome_usuario):
        user_id = ChatService.user_id_counter  # Atribui o ID atual ao usuário
        ChatService.user_id_counter += 1  # Incrementa o contador para o próximo usuário
        ChatService.users[user_id] = {"nome": nome_usuario, "na_sala": False}
        print(
            colorir_texto(
                f"[LOG] Usuário '{nome_usuario}' entrou no sistema com ID {user_id}.",
                "verde",
            )
        )
        return user_id

    # Método para o usuário entrar na sala de chat
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

    # Método para o usuário sair da sala
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

    # Método para enviar uma mensagem pública para a sala
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

    # Método para listar todas as mensagens públicas enviadas
    def exposed_listar_mensagens(self):
        return ChatService.messages

    # Método para enviar uma mensagem privada para outro usuário
    def exposed_enviar_mensagem_usuario(self, user_id, destinatario_id, mensagem):
        if user_id in ChatService.users and destinatario_id in ChatService.users:
            if user_id != destinatario_id:
                remetente_nome = ChatService.users[user_id]["nome"]
                destinatario_nome = ChatService.users[destinatario_id]["nome"]
                msg = f"{remetente_nome} para {destinatario_nome}: {mensagem}"

                # Adiciona a mensagem privada aos registros
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

    # Método para listar todos os usuários que estão na sala
    def exposed_listar_usuarios(self):
        usuarios_ativos = [
            user_info["nome"]
            for user_info in ChatService.users.values()
            if user_info["na_sala"]
        ]
        return usuarios_ativos

    # Método para listar todas as mensagens privadas de um usuário
    def exposed_listar_mensagens_privadas(self, user_id):
        return ChatService.private_messages.get(user_id, [])

    # Método para remover um usuário do sistema
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

    # Método para verificar se o usuário está na sala
    def exposed_verificar_status_usuario(self, user_id):
        if user_id in ChatService.users:
            return ChatService.users[user_id]["na_sala"]
        return False


# Inicia o servidor de chat
if __name__ == "__main__":
    t = ThreadedServer(
        ChatService, port=18861
    )  # Inicia o servidor com a classe ChatService
    print(colorir_texto("[SERVIDOR INICIADO] Aguardando conexões...", "azul"))
    t.start()  # Inicia o servidor para escutar conexões
