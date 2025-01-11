import hashlib
import json
from time import time


class Blockchain:
    def __init__(self):
        self.current_transactions = []  # Inicializa a lista de transações pendentes
        self.chain = []  # Inicializa a cadeia de blocos
        self.nodes = (
            set()
        )  # Inicializa o conjunto de nós (endpoints da rede blockchain)

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
            "timestamp": time(),  # Registro do horário de criação do bloco
            "transactions": self.current_transactions,  # Lista de transações pendentes que serão incluídas no bloco
            "proof": proof,  # Prova de trabalho que valida este bloco
            "previous_hash": previous_hash
            or self.hash(self.chain[-1]),  # Hash do bloco anterior
        }

        # Reinicia a lista de transações pendentes, pois elas já foram adicionadas ao bloco
        self.current_transactions = []

        self.chain.append(
            block
        )  # Adiciona o novo bloco à cadeia de blocos (self.chain)
        return block  # Retorna o bloco recém-criado

    def new_transaction(self, sender, recipient, amount):
        """
        Cria uma nova transação para ser incluída no próximo bloco minerado.

        :param sender: Endereço do remetente
        :param recipient: Endereço do destinatário
        :param amount: Valor da transação
        :return: O índice do bloco que irá conter esta transação
        """
        # Adiciona a nova transação à lista de transações pendentes
        self.current_transactions.append(
            {
                "remetente": sender,  # Endereço de quem está enviando
                "destinatario": recipient,  # Endereço de quem está recebendo
                "valor": amount,  # Quantia enviada
            }
        )

        # Retorna o índice do próximo bloco que conterá esta transação
        return self.last_block["index"] + 1

    @staticmethod
    def hash(block):
        """
        Cria um hash SHA-256 de um bloco.

        :param block: O bloco a ser transformado em hash
        """
        # Converte o bloco em uma string ordenada (para consistência no hashing)
        bloco_string = json.dumps(block, sort_keys=True).encode()

        # Retorna o hash SHA-256 da string do bloco
        return hashlib.sha256(bloco_string).hexdigest()

    @property
    def last_block(self):
        """
        Retorna o último bloco da cadeia.
        """
        return self.chain[-1]  # Acessa o último elemento da lista de blocos

    def proof_of_work(self, last_proof):
        """
        Algoritmo de Prova de Trabalho Simples:
        - Encontre um número p' tal que hash(pp') contenha 4 zeros à esquerda, onde p é a prova anterior.
        - p é a prova anterior e p' é a nova prova.

        :param last_proof: <int> A prova anterior.
        :return: <int> A nova prova encontrada.
        """
        proof = 0  # Inicializa a nova prova com 0.

        # Continua incrementando até encontrar uma prova válida.
        while self.valid_proof(last_proof, proof) is False:
            proof += 1  # Incrementa a prova a cada iteração.

        return proof  # Retorna a nova prova válida encontrada.

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Valida a prova.

        :param last_proof: <int> Prova anterior.
        :param proof: <int> Prova atual.
        :return: <bool> Verdadeiro se a prova for válida, Falso caso contrário.
        """
        # Concatena a prova anterior e a prova atual em uma string, depois codifica para bytes.
        tentativa = f"{last_proof}{proof}".encode()

        # Gera o hash SHA-256 da tentativa.
        hash_tentativa = hashlib.sha256(tentativa).hexdigest()

        # Verifica se os primeiros 4 caracteres do hash são "0000".
        return hash_tentativa[:4] == "0000"

    def valid_chain(self, chain):
        """
        Determina se um blockchain fornecido é válido.

        :param chain: <list> Um blockchain (lista de blocos).
        :return: <bool> Verdadeiro se o blockchain for válido, Falso caso contrário.
        """
        # Começa com o primeiro bloco da cadeia (genesis block).
        ultimo_bloco = chain[0]
        indice_atual = 1  # Índice para iterar pelos blocos subsequentes.

        # Itera por todos os blocos na cadeia.
        while indice_atual < len(chain):
            bloco = chain[indice_atual]  # Obtém o bloco atual.

            # Exibe os blocos para depuração e entendimento.
            print(f"Último bloco: {ultimo_bloco}")
            print(f"Bloco atual: {bloco}")
            print("\n-----------\n")

            # Verifica se o hash do bloco anterior está correto.
            if bloco["previous_hash"] != self.hash(ultimo_bloco):
                return False

            # Verifica se a Prova de Trabalho do bloco atual é válida.
            if not self.valid_proof(ultimo_bloco["proof"], bloco["proof"]):
                return False

            # Avança para o próximo bloco.
            ultimo_bloco = bloco
            indice_atual += 1

        # Se todos os blocos forem válidos, retorna True.
        return True

    def resolve_conflicts(self):
        """
        Este é o nosso algoritmo de consenso. Ele resolve conflitos
        substituindo nossa cadeia pela cadeia mais longa encontrada na rede.

        :return: <bool> True se nossa cadeia foi substituída, False caso contrário.
        """
        # Obtém os nós vizinhos na rede.
        vizinhos = self.nodes
        nova_cadeia = (
            None  # Inicializa uma variável para armazenar uma nova cadeia válida.
        )

        # Estamos interessados apenas em cadeias maiores que a nossa.
        comprimento_maximo = len(self.chain)

        # Solicita e verifica as cadeias de todos os nós na rede.
        for node in vizinhos:
            response = requests.get(
                f"http://{node}/chain"
            )  # Faz uma requisição HTTP para o nó.

            if response.status_code == 200:  # Verifica se a resposta foi bem-sucedida.
                comprimento = response.json()[
                    "length"
                ]  # Obtém o comprimento da cadeia do nó.
                cadeia = response.json()["chain"]  # Obtém a cadeia do nó.

                # Verifica se a cadeia do nó é maior e válida.
                if comprimento > comprimento_maximo and self.valid_chain(cadeia):
                    comprimento_maximo = comprimento  # Atualiza o comprimento máximo.
                    nova_cadeia = cadeia  # Atualiza a nova cadeia válida.

        # Substitui nossa cadeia se encontrarmos uma cadeia válida maior que a atual.
        if nova_cadeia:
            self.chain = nova_cadeia
            return True  # Retorna True indicando que a cadeia foi substituída.

        return False  # Retorna False se nenhuma cadeia foi substituída.
