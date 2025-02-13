# Casa Inteligente

Este projeto implementa um sistema de Casa Inteligente que utiliza MQTT para comunicação entre sensores, atuadores e controladores. As temperaturas são armazenadas em um banco de dados MongoDB, enquanto o estado do aquecedor (ligado ou desligado) é gerenciado com base nos dados recebidos. A solução também oferece um frontend simples para monitoramento e controle manual do sistema.

## Funcionalidades

- **Sensores**: Publicam a temperatura atual em intervalos regulares (a cada 5 segundos) via MQTT.
- **Atuadores**: Controlam o aquecedor com base na temperatura:
  - Se a temperatura for inferior a 15°C, o aquecedor é ligado.
  - Se a temperatura for superior a 22°C, ele é desligado.
- **Middleware**:
  - Recebe dados dos sensores via MQTT.
  - Armazena as temperaturas no banco de dados MongoDB.
  - Gerencia os comandos para o aquecedor.
- **Frontend**: Interface web que:
  - Exibe a temperatura atual e o status do aquecedor.
  - Permite o controle manual do aquecedor (ligar/desligar).

## Como Configurar e Executar

### 1. Instalar Dependências do Projeto

Certifique-se de que todas as dependências estão instaladas corretamente. Navegue até a pasta do projeto e execute:

```bash
npm install
```

Este comando irá baixar e instalar as dependências listadas no arquivo `package.json`.

### 2. Gerar Chaves de Segurança

Execute o script para gerar as chaves de segurança necessárias para a comunicação segura:

```bash
node config/generateKeys.js
```

### 3. Iniciar o Middleware (Servidor Express)

Inicie o servidor Express com o comando:

```bash
node middleware/server.js
```

O servidor estará disponível na porta 3000 para receber requisições do cliente.

### 4. Iniciar o Controlador Principal

Execute o controlador principal, que tomará decisões com base nos dados recebidos:

```bash
node controller/controller.js
```

### 5. Iniciar o Controlador Reserva

O controlador reserva serve como backup caso o controlador principal esteja indisponível. Para executá-lo:

```bash
node controller/backupController.js
```

### 6. Iniciar o Sensor

Para simular dados de temperatura, execute o sensor:

```bash
node sensor/sensor.js
```

### 7. Iniciar o Frontend

Abra o arquivo `client/index.html` em seu navegador utilizando a extensão [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer). O frontend irá exibir:

- A temperatura atualizada a cada 1 segundo.
- O status do aquecedor.
- Opção para controle manual do aquecedor.

## Tecnologias Utilizadas

- **MQTT**: Para comunicação entre sensores, atuadores e middleware.
- **MongoDB**: Para armazenamento das temperaturas e status do aquecedor.
- **Node.js**: Para execução do middleware e controladores.
- **Express**: Framework para criação do servidor web.
- **HTML/CSS/JavaScript**: Para criação da interface do cliente.
- **CORS**: Para permitir acesso do cliente ao servidor Express.

## Configuração de Variáveis de Ambiente

As configurações de MQTT podem ser ajustadas no arquivo `config/mqttConfig.js`. Certifique-se de configurar os detalhes corretos para conexão ao broker MQTT.

## Banco de Dados

O MongoDB é utilizado para armazenar dados de:

- **Temperatura**: Recebida dos sensores.
- **Status do Aquecedor**: Ligado ou desligado.

### Detalhes do Banco de Dados

- **Nome do Banco**: `casaInteligente`
- **Coleções**:
  - `temperatures`
  - `heaters`

Certifique-se de que o MongoDB está em execução antes de iniciar o middleware.
