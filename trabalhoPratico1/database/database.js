const { MongoClient } = require("mongodb"); // Importa o cliente MongoDB

const uri = "mongodb://localhost:27017"; // URI para conexão ao servidor MongoDB
let db; // Variável global para armazenar a instância do banco de dados

// Função para conectar ao banco de dados
async function connectToDb() {
  try {
    const client = new MongoClient(uri); // Cria uma nova instância do cliente MongoDB
    await client.connect(); // Conecta ao servidor MongoDB
    db = client.db("casaInteligente"); // Seleciona o banco de dados "casaInteligente"
    console.log("Conectado ao MongoDB");
  } catch (err) {
    console.error("Erro ao conectar ao MongoDB", err); // Loga o erro em caso de falha
    throw err; // Repassa o erro para interromper a execução
  }
}

// Função para registrar a temperatura no banco de dados
async function storeTemperature(temperature) {
  try {
    const collection = db.collection("temperatures"); // Acessa a coleção "temperatures"
    await collection.insertOne({
      value: temperature, // Armazena o valor da temperatura
      timestamp: new Date(), // Adiciona o timestamp atual
    });
  } catch (error) {
    console.error("Erro ao registrar temperatura", error); // Loga o erro em caso de falha
  }
}

// Função para atualizar o status do aquecedor no banco de dados
async function updateHeaterStatus(status) {
  try {
    const collection = db.collection("heaters"); // Acessa a coleção "heaters"
    await collection.insertOne({
      status, // Armazena o status do aquecedor (on/off)
      timestamp: new Date(), // Adiciona o timestamp atual
    });
  } catch (error) {
    console.error("Erro ao atualizar status do aquecedor", error); // Loga o erro em caso de falha
  }
}

// Função para obter o último status do aquecedor
async function getHeaterStatus() {
  try {
    const collection = db.collection("heaters"); // Acessa a coleção "heaters"
    const status = await collection.findOne({}, { sort: { timestamp: -1 } }); // Obtém o status mais recente
    return status ? status.status : "Desconhecido"; // Retorna o status ou "Desconhecido" se não encontrado
  } catch (error) {
    console.error("Erro ao obter status do aquecedor", error); // Loga o erro em caso de falha
  }
}

// Função para obter a última temperatura registrada
async function getTemperature() {
  try {
    const collection = db.collection("temperatures"); // Acessa a coleção "temperatures"
    const temp = await collection.findOne({}, { sort: { timestamp: -1 } }); // Obtém a temperatura mais recente
    return temp ? temp.value : null; // Retorna a temperatura ou null se não encontrada
  } catch (error) {
    console.error("Erro ao obter temperatura", error); // Loga o erro em caso de falha
  }
}

// Exporta as funções para uso em outros módulos
module.exports = {
  connectToDb, // Conectar ao banco de dados
  storeTemperature, // Registrar temperatura
  updateHeaterStatus, // Atualizar status do aquecedor
  getHeaterStatus, // Obter o status atual do aquecedor
  getTemperature, // Obter a temperatura mais recente
};
