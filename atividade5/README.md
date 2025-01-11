# Blockchain em Python

Este é um exemplo simples de um **Blockchain** implementado em **Python**. O sistema foi construído para fins educacionais, demonstrando como criar um blockchain, validar transações, minerar blocos e resolver conflitos entre cadeias.

## Tutorial utilizado

O tutorial original foi publicado por [Bimo Putro Tristianto](https://bimoputro.medium.com/) no Medium. O artigo original pode ser encontrado [aqui](https://bimoputro.medium.com/build-your-own-blockchain-in-python-a-practical-guide-f9620327ed03).

## Funcionalidades

- **Prova de Trabalho (PoW)**: O sistema usa o algoritmo de prova de trabalho para validar blocos.
- **Validação de Cadeia**: O blockchain pode verificar sua integridade e a validade de cada bloco.
- **Rede Peer-to-Peer**: O blockchain simula uma rede distribuída para resolver conflitos entre cadeias.
- **API HTTP**: Interaja com o blockchain usando uma API simples desenvolvida com Flask.

## Requisitos

- Python 3.x
- Flask

## Como Usar

1. Clone o repositório:

   ```bash
   git clone <URL_DO_REPOSITÓRIO>
   cd blockchain-python
   ```

2. Instale as dependências:

   ```bash
   pip install flask
   ```

3. Execute o servidor:

   ```bash
   python app.py
   ```

4. Interaja com o blockchain usando as rotas da API:

   - **POST** `/transactions/new`: Cria uma nova transação.
   - **GET** `/mine`: Minerar um novo bloco.
   - **GET** `/chain`: Obtém o blockchain completo.
