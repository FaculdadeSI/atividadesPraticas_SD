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
        pass  # Implementação será adicionada aqui

    @property
    def last_block(self):
        """
        Retorna o último bloco da cadeia.

        :return: O último bloco da blockchain
        """
        pass  # Implementação será adicionada aqui
