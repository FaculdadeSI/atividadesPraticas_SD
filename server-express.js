const express = require("express");
const fs = require("fs");
const path = require("path");
const app = express();

// Middleware para servir arquivos estáticos e para interpretar JSON
app.use(express.static(path.join(__dirname))); // Serve arquivos estáticos
app.use(express.json()); // Interpreta o corpo das requisições como JSON

// Middleware para todas as rotas que retorna os métodos permitidos
app.options('*', (req, res) => {
  console.log("Received OPTIONS request"); // Log para depuração
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS'); // Define os métodos permitidos
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type'); // Define os cabeçalhos permitidos
  res.sendStatus(200); // Retorna um status 200 OK
});

// Rota para a página inicial (HTML)
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html")); // Retorna a página inicial
});

// Rota para a página de registro (HTML)
app.get("/record", (req, res) => {
  res.sendFile(path.join(__dirname, "record.html")); // Retorna a página de registro
});

// Rota para criar um registro
app.post("/create", (req, res) => {
  const record = { ...req.body, id: Date.now() }; // Adiciona um ID único baseado no timestamp

  fs.readFile("data.txt", "utf8", (err, data) => {
    if (err) {
      console.error("Erro ao ler o arquivo:", err);
      return res.status(500).json({ error: "Erro ao ler o arquivo." }); // Erro ao ler o arquivo
    }

    let records = data ? JSON.parse(data) : []; // Inicializa a lista de registros
    records.push(record); // Adiciona o novo registro à lista

    fs.writeFile("data.txt", JSON.stringify(records, null, 2), (err) => {
      if (err) {
        console.error("Erro ao escrever no arquivo:", err);
        return res.status(500).json({ error: "Erro ao escrever no arquivo." }); // Erro ao escrever no arquivo
      }

      res.json(record); // Retorna o novo registro criado
    });
  });
});

// Rota para buscar registros pelo nome
app.get("/queryByName", (req, res) => {
  const name = req.query.name; // Obtém o nome da consulta

  fs.readFile("data.txt", "utf8", (err, data) => {
    if (err) {
      console.error("Erro ao ler o arquivo:", err);
      return res.status(500).json({ error: "Erro ao ler o arquivo." }); // Erro ao ler o arquivo
    }

    const records = data ? JSON.parse(data) : []; // Inicializa a lista de registros
    const matchedRecords = records.filter((r) => r.name === name); // Filtra registros pelo nome

    if (matchedRecords.length > 0) {
      return res.json(matchedRecords); // Retorna registros encontrados
    }

    return res.status(404).json({ error: "Nenhum registro encontrado." }); // Retorno se não houver registros
  });
});

// Rota para buscar um registro pelo ID
app.get("/query", (req, res) => {
  const id = req.query.id; // Obtém o ID da consulta

  fs.readFile("data.txt", "utf8", (err, data) => {
    if (err) {
      console.error("Erro ao ler o arquivo:", err);
      return res.status(500).json({ error: "Erro ao ler o arquivo." }); // Erro ao ler o arquivo
    }

    const records = data ? JSON.parse(data) : []; // Inicializa a lista de registros
    const record = records.find((r) => r.id == id); // Encontra o registro pelo ID

    if (record) {
      return res.json(record); // Retorna o registro encontrado
    }

    return res.status(404).json({ error: "Registro não encontrado." }); // Retorno se não houver registro
  });
});

// Rota para atualizar um registro
app.put("/update", (req, res) => {
  const recordToUpdate = req.body; // Obtém os dados do registro a ser atualizado

  fs.readFile("data.txt", "utf8", (err, data) => {
    if (err) {
      console.error("Erro ao ler o arquivo:", err);
      return res.status(500).json({ error: "Erro ao ler o arquivo." }); // Erro ao ler o arquivo
    }

    let records = data ? JSON.parse(data) : []; // Inicializa a lista de registros
    const recordIndex = records.findIndex((r) => r.id == recordToUpdate.id); // Encontra o índice do registro

    if (recordIndex === -1) {
      return res.status(404).json({ error: "Registro não encontrado." }); // Retorno se não houver registro
    }

    records[recordIndex] = recordToUpdate; // Atualiza o registro encontrado

    fs.writeFile("data.txt", JSON.stringify(records, null, 2), (err) => {
      if (err) {
        console.error("Erro ao escrever no arquivo:", err);
        return res.status(500).json({ error: "Erro ao escrever no arquivo." }); // Erro ao escrever no arquivo
      }

      res.json(recordToUpdate); // Retorna o registro atualizado
    });
  });
});

// Rota para atualizar um registro parcialmente
app.patch("/updatePartial", (req, res) => {
  const recordToUpdate = req.body; // Obtém os dados do registro a ser atualizado parcialmente

  fs.readFile("data.txt", "utf8", (err, data) => {
    if (err) {
      console.error("Erro ao ler o arquivo:", err);
      return res.status(500).json({ error: "Erro ao ler o arquivo." }); // Erro ao ler o arquivo
    }

    let records = data ? JSON.parse(data) : []; // Inicializa a lista de registros
    const recordIndex = records.findIndex((r) => r.id == recordToUpdate.id); // Encontra o índice do registro

    if (recordIndex === -1) {
      return res.status(404).json({ error: "Registro não encontrado." }); // Retorno se não houver registro
    }

    // Atualiza apenas os campos que foram fornecidos no corpo da requisição
    const updatedRecord = { ...records[recordIndex], ...recordToUpdate };
    records[recordIndex] = updatedRecord; // Atualiza o registro encontrado

    fs.writeFile("data.txt", JSON.stringify(records, null, 2), (err) => {
      if (err) {
        console.error("Erro ao escrever no arquivo:", err);
        return res.status(500).json({ error: "Erro ao escrever no arquivo." }); // Erro ao escrever no arquivo
      }

      res.json(updatedRecord); // Retorna o registro atualizado
    });
  });
});

// Rota para excluir um registro
app.delete("/delete", (req, res) => {
  const id = req.body.id; // Obtém o ID do corpo da requisição

  fs.readFile("data.txt", "utf8", (err, data) => {
    if (err) {
      console.error("Erro ao ler o arquivo:", err);
      return res.status(500).json({ error: "Erro ao ler o arquivo." }); // Erro ao ler o arquivo
    }

    let records = data ? JSON.parse(data) : []; // Inicializa a lista de registros
    records = records.filter((r) => r.id != id); // Remove o registro com o ID correspondente

    fs.writeFile("data.txt", JSON.stringify(records, null, 2), (err) => {
      if (err) {
        console.error("Erro ao escrever no arquivo:", err);
        return res.status(500).json({ error: "Erro ao escrever no arquivo." }); // Erro ao escrever no arquivo
      }

      res.json({ message: "Registro excluído com sucesso!" }); // Retorna mensagem de sucesso
    });
  });
});

// Inicia o servidor na porta 3000
app.listen(3000, () => {
  console.log("Servidor rodando na porta 3000"); // Log para depuração
});
