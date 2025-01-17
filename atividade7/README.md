# Blockchain em Python

Este é um exemplo simples de um **Blockchain** implementado em **Python**. O sistema foi construído para fins educacionais, demonstrando como criar um blockchain, validar transações, minerar blocos, resolver conflitos entre cadeias e interagir com a blockchain por meio de uma API.

## Tutorial utilizado

O tutorial original foi publicado por [Bimo Putro Tristianto](https://bimoputro.medium.com/) no Medium. O artigo original pode ser encontrado [aqui](https://bimoputro.medium.com/build-your-own-blockchain-in-python-a-practical-guide-f9620327ed03).

## Funcionalidades

- **Prova de Trabalho (PoW)**: O sistema usa o algoritmo de prova de trabalho para validar blocos.
- **Validação de Cadeia**: O blockchain pode verificar sua integridade e a validade de cada bloco.
- **Rede Peer-to-Peer**: O blockchain simula uma rede distribuída para resolver conflitos entre cadeias.
- **API HTTP**: Interaja com o blockchain usando uma API simples desenvolvida com Flask. A API expõe os seguintes endpoints:
  - **POST** `/transactions/new`: Cria uma nova transação.
  - **GET** `/mine`: Minerar um novo bloco.
  - **GET** `/chain`: Obtém o blockchain completo.
  - **POST** `/nodes/register`: Registra novos nós na rede.
  - **GET** `/nodes/resolve`: Resolve conflitos e garante a integridade da cadeia.

## Requisitos

- Python 3.x
- Flask

## Como Usar

### 1. Clone o repositório:

```bash
git clone https://github.com/FaculdadeSI/atividadesPraticas_SD.git
cd atividadesPraticas_SD
cd atividade5
```

### 2. Instale as dependências:

```bash
pip3 install --break-system-packages flask
```

### 3. Execute o servidor:

```bash
python api.py
```

O servidor estará executando na porta **5001** por padrão.

### 4. Interaja com o blockchain usando as rotas da API:

- **POST** `/transactions/new`: Cria uma nova transação.

  - Corpo da requisição (JSON):
    ```json
    {
      "sender": "endereço_do_remetente",
      "recipient": "endereço_do_destinatário",
      "amount": "valor"
    }
    ```

- **GET** `/mine`: Minerar um novo bloco e adicionar à blockchain.

- **GET** `/chain`: Obtém o blockchain completo, incluindo todos os blocos minerados.

- **POST** `/nodes/register`: Registra novos nós na rede.

  - Corpo da requisição (JSON):
    ```json
    {
      "nodes": ["http://192.168.1.2:5000", "http://192.168.1.3:5000"]
    }
    ```

- **GET** `/nodes/resolve`: Resolve conflitos na rede, substituindo a cadeia local pela cadeia mais longa e válida.

## Explicação do Código

- **Blockchain**: A classe `Blockchain` contém todos os métodos necessários para criar, minerar e validar blocos. Ela também gerencia as transações e a resolução de conflitos entre diferentes instâncias da blockchain.
- **Prova de Trabalho (PoW)**: O sistema utiliza um algoritmo de mineração baseado em Prova de Trabalho para encontrar um valor (prova) que, quando combinado com o bloco anterior, gera um hash com uma condição específica (quatro zeros à esquerda).

- **API Flask**: A API é desenvolvida usando Flask e fornece endpoints para interagir com a blockchain. Cada operação, como adicionar transações, minerar blocos e consultar a cadeia, é acessada via HTTP.
