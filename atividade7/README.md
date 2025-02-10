# 🚀 Blockchain em Python

Este é um exemplo simples de um **Blockchain** implementado em **Python**, utilizando **Flask** para criar uma API interativa. O sistema foi desenvolvido para fins educacionais, demonstrando como criar um blockchain, validar transações, minerar blocos, resolver conflitos entre cadeias e interagir por meio de uma interface web.

## 📌 Funcionalidades

✅ **Prova de Trabalho (PoW)**: Algoritmo de mineração para validar blocos.  
✅ **Validação de Cadeia**: Garante a integridade e a validade dos blocos.  
✅ **Rede Peer-to-Peer**: Sincronização automática entre diferentes nós.  
✅ **API HTTP**: Criada com Flask para interagir com a blockchain.  
✅ **Interface Web**: Desenvolvida com HTML, CSS e JavaScript para facilitar a interação.  
✅ **Registro Automático de Nós**: Cada API registra automaticamente os outros nós na rede.  
✅ **Sincronização Automática**: Sempre que uma nova transação é criada, a mineração e a resolução de conflitos são disparadas automaticamente.

---

## 🛠️ Requisitos

- **Python 3.x**
- **Flask** para a API

---

## 🚀 Como Executar

### 1️⃣ Clone o repositório:

```bash
git clone https://github.com/FaculdadeSI/atividadesPraticas_SD.git
cd atividadesPraticas_SD/atividade7
```

### 2️⃣ Instale as dependências:

```bash
pip3 install --break-system-packages flask
```

### 3️⃣ Execute as três APIs em terminais diferentes:

```bash
# No primeiro terminal (API 1)
python3 api1/api.py 
```

```bash
# No segundo terminal (API 2)
python3 api2/api2.py 
```

```bash
# No terceiro terminal (API 3)
python3 api3/api3.py 
```

Cada API rodará em uma porta diferente:

- **API 1**: `http://127.0.0.1:5001`
- **API 2**: `http://127.0.0.1:5002`
- **API 3**: `http://127.0.0.1:5003`

### 4️⃣ Acesse a interface web:

Abra o navegador e vá até `http://127.0.0.1:5500/api1/api.html`, `http://127.0.0.1:5500/api2/api2.html` e `http://127.0.0.1:5500/api3/api3.html` para interagir com a blockchain.

---

## 🔗 Como Funciona?

A blockchain está distribuída entre três nós, e a sincronização ocorre automaticamente:

1️⃣ **Criação de Transação**:

- O usuário preenche o remetente, destinatário e valor e clica em **Criar Transação**.
- A transação é enviada para o nó principal (URL principal no HTML que o usuário estiver utilizando).

2️⃣ **Mineração Automática**:

- Após criar a transação, a mineração do bloco acontece automaticamente.

3️⃣ **Sincronização Automática**:

- Após a mineração, a API chama `/nodes/resolve` para garantir que todas as três APIs tenham a mesma cadeia.

---

## 🌍 **Endpoints da API**

### 📌 Criar Transação

**POST** `/transactions/new`  
Cria uma nova transação e a adiciona ao bloco atual.

**Corpo da requisição (JSON)**:

```json
{
  "sender": "Teste 1",
  "recipient": "Teste 2",
  "amount": 10
}
```

---

### 📌 Minerar Bloco

**GET** `/mine`  
Executa a prova de trabalho e adiciona um novo bloco à blockchain.

---

### 📌 Obter Blockchain

**GET** `/chain`  
Retorna a blockchain completa em formato JSON.

---

### 📌 Registrar Nós

**POST** `/nodes/register`  
Registra novos nós na rede. O sistema já faz isso automaticamente no início.

**Corpo da requisição (JSON)**:

```json
{
  "nodes": ["http://127.0.0.1:5002", "http://127.0.0.1:5003"]
}
```

---

### 📌 Resolver Conflitos

**GET** `/nodes/resolve`  
Sincroniza a blockchain entre os nós, garantindo que todos tenham a cadeia mais longa válida.
