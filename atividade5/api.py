from uuid import uuid4
from blockchain import Blockchain
from flask import Flask

# Cria uma instância do aplicativo Flask
app = Flask(__name__)

# Gera um endereço globalmente único para este nó
node_identifier = str(uuid4()).replace("-", "")

# Instancia o objeto Blockchain
blockchain = Blockchain()
