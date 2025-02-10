from urllib import request
from uuid import uuid4
from blockchain import Blockchain
from flask import Flask, jsonify, request
from flask_cors import CORS

# Cria uma instância do aplicativo Flask para criar a API
app = Flask(__name__)
CORS(app)


# Gera um identificador único global para este nó (usado para distinguir entre diferentes nós na rede)
node_identifier = str(uuid4()).replace(
    "-", ""
)  # Um identificador único para o nó atual

# Instancia o objeto Blockchain que irá gerenciar a cadeia de blocos
blockchain = Blockchain()


# TODO: criei
# Adiciona a rota padrão para a raiz do servidor
@app.route("/", methods=["GET"])
def home():
    # Retorna uma mensagem de boas-vindas quando o servidor é acessado
    return "Welcome to the Blockchain API!"


@app.route("/mine", methods=["GET"])
def mine():
    """
    Esta rota simula a mineração de um novo bloco na blockchain.
    Ela executa a Prova de Trabalho (Proof of Work) para encontrar a prova,
    cria uma nova transação e adiciona um novo bloco à blockchain.
    """
    # Obtém o último bloco da cadeia
    last_block = blockchain.last_block

    # Executa o algoritmo de Prova de Trabalho para encontrar a nova prova
    proof = blockchain.proof_of_work(last_block)

    # Cria uma transação que recompensa o minerador. O remetente é "0", indicando que é uma recompensa.
    blockchain.new_transaction(
        sender="0",  # "0" significa que a transação é uma recompensa por minerar
        recipient=node_identifier,  # O minerador recebe a recompensa
        amount=1,  # A recompensa por minerar um bloco
    )

    # Adiciona o novo bloco à cadeia com a nova prova e o hash do bloco anterior
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    # Retorna os dados do novo bloco minerado
    response = {
        "message": "Novo Bloco Forjado",  # Mensagem indicando que o bloco foi minerado
        "index": block["index"],  # Índice do bloco na cadeia
        "transactions": block["transactions"],  # Transações incluídas no bloco
        "proof": block["proof"],  # Prova de trabalho que valida o bloco
        "previous_hash": block["previous_hash"],  # Hash do bloco anterior
    }
    return jsonify(response), 200  # Retorna a resposta em formato JSON


@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    """
    Esta rota permite a criação de uma nova transação.
    Os dados da transação são enviados no corpo da requisição (JSON).
    """
    values = request.get_json()  # Obtém os dados enviados no corpo da requisição

    # Verifica se os campos obrigatórios estão presentes
    required = ["sender", "recipient", "amount"]
    if not all(k in values for k in required):
        return "Faltando valores", 400  # Retorna erro caso algum campo esteja faltando

    # Cria a transação e a adiciona à blockchain
    index = blockchain.new_transaction(
        values["sender"], values["recipient"], values["amount"]
    )

    # Responde com a confirmação da transação
    response = {"message": f"A transação será adicionada ao Bloco {index}"}
    return jsonify(response), 201  # Retorna a resposta com status 201 (Criado)


@app.route("/chain", methods=["GET"])
def full_chain():
    """
    Esta rota retorna toda a cadeia de blocos da blockchain.
    """
    response = {
        "chain": blockchain.chain,  # A cadeia de blocos atual
        "length": len(blockchain.chain),  # O número de blocos na cadeia
    }
    return jsonify(response), 200  # Retorna a resposta com os dados da cadeia


@app.route("/nodes/register", methods=["POST"])
def register_nodes():
    """
    Esta rota permite registrar novos nós na rede.
    Os nós são fornecidos como uma lista no corpo da requisição.
    """
    values = request.get_json()  # Obtém os dados enviados no corpo da requisição

    # Recupera a lista de nós fornecida
    nodes = values.get("nodes")

    # Verifica se a lista de nós foi fornecida corretamente
    if nodes is None:
        return (
            "Erro: Forneça uma lista válida de nós",
            400,
        )  # Retorna erro caso não haja nós fornecidos

    # Registra cada nó fornecido na blockchain
    for node in nodes:
        blockchain.register_node(node)

    # Responde com a lista de nós registrados
    response = {
        "message": "Novos nós foram adicionados",
        "total_nodes": list(blockchain.nodes),  # Lista de todos os nós registrados
    }
    return jsonify(response), 201  # Retorna a resposta com status 201 (Criado)


@app.route("/nodes/resolve", methods=["GET"])
def consensus():
    """
    Esta rota implementa o algoritmo de consenso da blockchain.
    Ele tenta resolver conflitos verificando se há uma cadeia maior e válida na rede.
    """
    # Tenta resolver conflitos e atualizar a cadeia, caso necessário
    replaced = blockchain.resolve_conflicts()

    # Se a cadeia foi substituída por uma maior e válida, retorna a nova cadeia
    if replaced:
        response = {
            "message": "Nossa cadeia foi substituída",  # Mensagem indicando que a cadeia foi substituída
            "new_chain": blockchain.chain,  # A nova cadeia maior e válida
        }
    else:
        # Caso contrário, a cadeia local é considerada a autoritativa
        response = {"message": "Nossa cadeia é autoritativa", "chain": blockchain.chain}

    return jsonify(response), 200  # Retorna a resposta com os dados da cadeia


# Se este arquivo for executado diretamente, inicia o servidor Flask
if __name__ == "__main__":
    # Registra os nós automaticamente ao iniciar a API
    known_nodes = ["http://127.0.0.1:5001", "http://127.0.0.1:5003"]
    blockchain.register_node(
        "http://127.0.0.1:5002"
    )  # Garante que o próprio nó está registrado
    for node in known_nodes:
        blockchain.register_node(node)

    print(f"Nós registrados automaticamente: {list(blockchain.nodes)}")
    app.run(host="0.0.0.0", port=5002)
