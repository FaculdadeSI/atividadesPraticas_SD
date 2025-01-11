from urllib import request
from uuid import uuid4
from blockchain import Blockchain
from flask import Flask

# Cria uma instância do aplicativo Flask
app = Flask(__name__)

# Gera um endereço globalmente único para este nó
node_identifier = str(uuid4()).replace("-", "")

# Instancia o objeto Blockchain
blockchain = Blockchain()


@app.route("/mine", methods=["GET"])
def mine():
    # Executamos o algoritmo de prova de trabalho para obter a próxima prova...
    ultimo_bloco = blockchain.last_block
    prova = blockchain.proof_of_work(ultimo_bloco)

    # Devemos receber uma recompensa por encontrar a prova.
    # O remetente é "0" para indicar que este nó minerou uma nova moeda.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forjamos o novo bloco adicionando-o à cadeia
    hash_anterior = blockchain.hash(ultimo_bloco)
    bloco = blockchain.new_block(prova, hash_anterior)

    response = {
        "message": "Novo Bloco Forjado",
        "index": bloco["index"],
        "transactions": bloco["transactions"],
        "proof": bloco["proof"],
        "previous_hash": bloco["previous_hash"],
    }
    return jsonify(response), 200


@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.get_json()

    # Verifica se os campos obrigatórios estão nos dados enviados via POST
    required = ["sender", "recipient", "amount"]
    if not all(k in values for k in required):
        return "Faltando valores", 400

    # Cria uma nova Transação
    index = blockchain.new_transaction(
        values["sender"], values["recipient"], values["amount"]
    )

    response = {"message": f"A transação será adicionada ao Bloco {index}"}
    return jsonify(response), 201


@app.route("/chain", methods=["GET"])
def full_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
    return jsonify(response), 200
