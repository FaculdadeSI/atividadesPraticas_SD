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


# Adiciona a rota padrão para a raiz do servidor
@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Blockchain API!"


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


@app.route("/nodes/register", methods=["POST"])
def register_nodes():
    # Obtém os dados enviados no corpo da requisição em formato JSON
    values = request.get_json()

    # Recupera a lista de nós fornecida
    nodes = values.get("nodes")

    # Verifica se a lista de nós foi fornecida corretamente
    if nodes is None:
        return "Erro: Forneça uma lista válida de nós", 400

    # Registra cada nó fornecido na blockchain
    for node in nodes:
        blockchain.register_node(node)

    # Resposta confirmando a adição dos novos nós
    response = {
        "message": "Novos nós foram adicionados",
        "total_nodes": list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route("/nodes/resolve", methods=["GET"])
def consensus():
    # Tenta resolver conflitos na blockchain verificando se há uma cadeia maior e válida
    substituted = blockchain.resolve_conflicts()

    # Se a cadeia foi substituída por uma cadeia maior, retorna a nova cadeia
    if substituted:
        response = {
            "message": "Nossa cadeia foi substituída",
            "new_chain": blockchain.chain,
        }
    else:
        # Se não houver substituição, a cadeia atual é a autoritativa
        response = {"message": "Nossa cadeia é autoritativa", "chain": blockchain.chain}

    return jsonify(response), 200


# Se este arquivo for executado diretamente, inicia o servidor Flask
if __name__ == "__main__":
    # Inicia o servidor na máquina local, ouvindo na porta 5000
    app.run(host="0.0.0.0", port=5001)
