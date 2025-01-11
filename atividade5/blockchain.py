import hashlib
import json
from time import time


class Blockchain:
    def __init__(self):
        self.current_transactions = [] # Inicializa a lista de transações pendentes
        self.chain = [] # Inicializa a cadeia de blocos
        self.nodes = set() # Inicializa o conjunto de nós (endpoints da rede blockchain)

        # Cria o bloco gênese (primeiro bloco da blockchain)
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Cria um novo bloco na blockchain.

        :param proof: A prova fornecida pelo algoritmo de Prova de Trabalho (Proof of Work)
        :param previous_hash: Hash do bloco anterior
        :return: O novo bloco
        """
        pass  # Implementação será adicionada aqui

    def new_transaction(self, sender, recipient, amount):
        """
        Cria uma nova transação para ser adicionada ao próximo bloco minerado.

        :param sender: Endereço do remetente
        :param recipient: Endereço do destinatário
        :param amount: Valor da transação
        :return: O índice do bloco que conterá essa transação
        """
        pass  # Implementação será adicionada aqui

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
