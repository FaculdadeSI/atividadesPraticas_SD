import hashlib
import json
import requests
from time import time


class Blockchain:
    def __init__(self):
        """
        Inicializa a blockchain, criando um bloco gênese e
        configurando listas e variáveis necessárias para transações
        e validação de blocos.
        """
        self.current_transactions = []  # Lista de transações pendentes
        self.chain = []  # Cadeia de blocos
        self.nodes = set()  # Conjunto de nós na rede blockchain

        # Cria o bloco gênese (primeiro bloco da blockchain)
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Cria um novo bloco na Blockchain.

        :param proof: A prova fornecida pelo algoritmo de Prova de Trabalho (Proof of Work)
        :param previous_hash: O hash do bloco anterior
        :return: O novo bloco criado
        """
        # Define a estrutura do novo bloco como um dicionário
        block = {
            "index": len(self.chain) + 1,  # Índice do bloco (posição na cadeia)
            "timestamp": time(),  # Horário de criação do bloco
            "transactions": self.current_transactions,  # Transações a serem incluídas no bloco
            "proof": proof,  # Prova de trabalho que valida o bloco
            "previous_hash": previous_hash
            or self.hash(self.chain[-1]),  # Hash do bloco anterior
        }

        self.current_transactions = []  # Reinicia as transações pendentes
        self.chain.append(block)  # Adiciona o novo bloco à cadeia
        return block  # Retorna o bloco recém-criado

    def new_transaction(self, sender, recipient, amount):
        """
        Cria uma nova transação para ser incluída no próximo bloco minerado.

        :param sender: Endereço do remetente
        :param recipient: Endereço do destinatário
        :param amount: Valor da transação
        :return: Índice do bloco que conterá esta transação
        """
        # Adiciona a nova transação à lista de transações pendentes
        self.current_transactions.append(
            {
                "remetente": sender,  # Endereço de quem está enviando
                "destinatario": recipient,  # Endereço de quem está recebendo
                "valor": amount,  # Quantia enviada
            }
        )

        return self.last_block["index"] + 1  # Retorna o índice do próximo bloco

    @staticmethod
    def hash(block):
        """
        Cria um hash SHA-256 de um bloco.

        :param block: O bloco a ser transformado em hash
        :return: O hash do bloco
        """
        bloco_string = json.dumps(
            block, sort_keys=True
        ).encode()  # Converte o bloco para uma string
        return hashlib.sha256(bloco_string).hexdigest()  # Retorna o hash SHA-256

    @property
    def last_block(self):
        """
        Retorna o último bloco da cadeia.
        """
        return self.chain[-1]  # Acessa o último elemento da lista de blocos

    def proof_of_work(self, last_block):
        """
        Algoritmo de Prova de Trabalho (Proof of Work) do Bitcoin:
        Encontra um número 'p' tal que o hash de (p + p') contenha 4 zeros à esquerda.

        :param last_block: O último bloco.
        :return: A nova prova encontrada.
        """
        # Obtém a prova anterior do último bloco.
        ultima_prova = last_block["proof"]

        # Calcula o hash do último bloco.
        ultimo_hash = self.hash(last_block)

        # Inicializa a nova prova como 0.
        prova = 0

        # Encontra a nova prova válida
        while self.valid_proof(ultima_prova, prova, ultimo_hash) is False:
            prova += 1

        return prova  # Retorna a nova prova encontrada

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Valida a Prova de Trabalho.

        :param last_proof: A prova anterior.
        :param proof: A prova atual.
        :param last_hash: O hash do último bloco.
        :return: True se a prova for válida, False caso contrário.
        """
        tentativa = (
            f"{last_proof}{proof}{last_hash}".encode()
        )  # Concatena as provas e o hash
        tentativa_hash = hashlib.sha256(
            tentativa
        ).hexdigest()  # Calcula o hash da tentativa

        return tentativa_hash[:4] == "0000"  # Verifica se o hash começa com 4 zeros

    def valid_chain(self, chain):
        """
        Determina se um blockchain fornecido é válido.

        :param chain: Um blockchain (lista de blocos).
        :return: True se o blockchain for válido, False caso contrário.
        """
        ultimo_bloco = chain[0]  # Começa com o primeiro bloco da cadeia (genesis block)
        indice_atual = 1  # Índice para iterar pelos blocos subsequentes

        # Itera pelos blocos da cadeia
        while indice_atual < len(chain):
            bloco = chain[indice_atual]  # Obtém o bloco atual.

            # Exibe os blocos para depuração e entendimento.
            print(f"Último bloco: {ultimo_bloco}")
            print(f"Bloco atual: {bloco}")
            print("\n-----------\n")

            # Verifica se o hash do bloco anterior está correto
            if bloco["previous_hash"] != self.hash(ultimo_bloco):
                return False

            # Verifica se a Prova de Trabalho do bloco atual é válida
            if not self.valid_proof(ultimo_bloco["proof"], bloco["proof"]):
                return False

            # Avança para o próximo bloco.
            ultimo_bloco = bloco
            indice_atual += 1

        return True  # Se todos os blocos forem válidos, retorna True

    def resolve_conflicts(self):
        """
        Resolve conflitos substituindo nossa cadeia pela cadeia mais longa encontrada na rede.

        :return: True se nossa cadeia foi substituída, False caso contrário.
        """
        vizinhos = self.nodes  # Obtém os nós vizinhos na rede
        nova_cadeia = (
            None  # Inicializa uma variável para armazenar uma nova cadeia válida
        )
        comprimento_maximo = len(self.chain)  # Comprimento máximo da cadeia atual

        # Estamos interessados apenas em cadeias maiores que a nossa.
        comprimento_maximo = len(self.chain)

        # Solicita e verifica as cadeias de todos os nós na rede.
        for node in vizinhos:
            response = requests.get(
                f"{node}/chain"
            )  # Faz uma requisição HTTP para o nó

            if response.status_code == 200:  # Se a resposta for bem-sucedida
                comprimento = response.json()["length"]  # Obtém o comprimento da cadeia
                cadeia = response.json()["chain"]  # Obtém a cadeia do nó

                # Verifica se a cadeia do nó é maior e válida
                if comprimento > comprimento_maximo and self.valid_chain(cadeia):
                    comprimento_maximo = comprimento  # Atualiza o comprimento máximo
                    nova_cadeia = cadeia  # Atualiza a nova cadeia válida

        # Substitui a cadeia local pela nova cadeia mais longa encontrada
        if nova_cadeia:
            self.chain = nova_cadeia
            return True  # A cadeia foi substituída

        return False  # Nenhuma cadeia foi substituída

    def register_node(self, node):
        """
        Adiciona um novo nó à lista de nós.

        :param node: Endereço do nó (ex: 'http://192.168.1.2:5000')
        """
        self.nodes.add(node)  # Adiciona o nó ao conjunto de nós
