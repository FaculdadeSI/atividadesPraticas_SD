const express = require("express"); // Importa o framework Express
const cors = require("cors"); // Middleware para permitir requisições de diferentes origens
const {
  connectToDb,
  getHeaterStatus,
  getTemperature,
  updateHeaterStatus,
} = require("../database/database"); // Funções do banco de dados

const app = express(); // Inicializa o servidor Express
const port = 3000; // Define a porta do servidor

// Middleware para habilitar CORS (Cross-Origin Resource Sharing)
app.use(cors());
// Middleware para processar requisições com corpo no formato JSON
app.use(express.json());
// Middleware para processar requisições com dados codificados na URL
app.use(express.urlencoded({ extended: true }));

// Função auto-executável para inicializar o servidor
(async function initializeServer() {
  await connectToDb(); // Conecta ao banco de dados antes de iniciar o servidor

  // Endpoint para obter o status atual do aquecedor
  app.get("/heater-status", async (req, res) => {
    try {
      const status = await getHeaterStatus(); // Consulta o banco de dados
      res.json({ status }); // Retorna o status em formato JSON
    } catch (error) {
      res.status(500).json({ error: "Erro ao obter o status do aquecedor" }); // Resposta de erro
    }
  });

  // Endpoint para obter a temperatura mais recente
  app.get("/temperature", async (req, res) => {
    try {
      const temperature = await getTemperature(); // Consulta o banco de dados
      res.json({ temperature }); // Retorna a temperatura em formato JSON
    } catch (error) {
      res.status(500).json({ error: "Erro ao obter a temperatura" }); // Resposta de erro
    }
  });

  // Endpoint para processar comandos para o aquecedor (ligar/desligar)
  app.post("/heater-command", async (req, res) => {
    try {
      const { command } = req.body; // Extrai o comando do corpo da requisição
      if (!command) {
        return res.status(400).json({ error: "Comando não fornecido" }); // Verifica se o comando foi enviado
      }
      // Atualiza o status do aquecedor no banco de dados
      await updateHeaterStatus(command);
      // Responde ao cliente com sucesso
      res.json({ message: `Comando "${command}" recebido com sucesso` });
    } catch (error) {
      console.error("Erro ao processar o comando:", error); // Loga o erro
      res.status(500).json({ error: "Erro ao processar o comando" }); // Resposta de erro
    }
  });

  // Inicia o servidor e escuta na porta especificada
  app.listen(port, () => {
    console.log(`Servidor rodando na porta ${port}`);
  });
})();
