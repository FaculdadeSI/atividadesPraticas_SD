const express = require("express");
const fs = require("fs");
const path = require("path");
const app = express();

// Middleware para servir arquivos estáticos
app.use(express.static(path.join(__dirname)));
app.use(express.json());

// Rota para a página inicial (HTML)
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

// Rota para a página de registro (HTML)
app.get("/record", (req, res) => {
  res.sendFile(path.join(__dirname, "record.html"));
});

// Rota para criar um registro
app.post("/create", (req, res) => {
  const record = { ...req.body, id: Date.now() }; // Adiciona um ID único baseado no timestamp
  console.log("Criando registro:", record);

  fs.readFile("data.txt", "utf8", (err, data) => {
    if (err) {
      console.error("Erro ao ler o arquivo:", err);
      return res.status(500).json({ error: "Erro ao ler o arquivo." });
    }
    let records = data ? JSON.parse(data) : [];
    records.push(record);
    fs.writeFile("data.txt", JSON.stringify(records, null, 2), (err) => {
      if (err) {
        console.error("Erro ao escrever no arquivo:", err);
        return res.status(500).json({ error: "Erro ao escrever no arquivo." });
      }
      console.log("Registro criado com sucesso!");
      res.json(record);
    });
  });
});

// Rota para buscar registros pelo nome
app.get("/queryByName", (req, res) => {
  const name = req.query.name; // Obtém o nome
  console.log("Buscando registros por nome:", name);

  fs.readFile("data.txt", "utf8", (err, data) => {
    if (err) {
      console.error("Erro ao ler o arquivo:", err);
      return res.status(500).json({ error: "Erro ao ler o arquivo." });
    }
    const records = data ? JSON.parse(data) : [];
    const matchedRecords = records.filter((r) => r.name === name); // Compara com o nome
    if (matchedRecords.length > 0) {
      return res.json(matchedRecords); // Retorna todos os registros encontrados
    }
    return res.status(404).json({ error: "Nenhum registro encontrado." });
  });
});

// Rota para buscar um registro pelo ID (adicionada)
app.get("/query", (req, res) => {
  const id = req.query.id; // Obtém o ID
  console.log("Buscando registro por ID:", id);

  fs.readFile("data.txt", "utf8", (err, data) => {
    if (err) {
      console.error("Erro ao ler o arquivo:", err);
      return res.status(500).json({ error: "Erro ao ler o arquivo." });
    }
    const records = data ? JSON.parse(data) : [];
    const record = records.find((r) => r.id == id); // Compara com o ID
    if (record) {
      return res.json(record); // Retorna o registro encontrado
    }
    return res.status(404).json({ error: "Registro não encontrado." });
  });
});

// Rota para atualizar um registro (PUT)
app.put("/update", (req, res) => {
  const recordToUpdate = req.body;
  console.log("Atualizando registro:", recordToUpdate);

  fs.readFile("data.txt", "utf8", (err, data) => {
    if (err) {
      console.error("Erro ao ler o arquivo:", err);
      return res.status(500).json({ error: "Erro ao ler o arquivo." });
    }

    let records = data ? JSON.parse(data) : [];
    const recordIndex = records.findIndex((r) => r.id == recordToUpdate.id);

    if (recordIndex === -1) {
      return res.status(404).json({ error: "Registro não encontrado." });
    }

    // Atualiza todos os campos
    records[recordIndex] = recordToUpdate; // Substitui o registro antigo pelo novo

    fs.writeFile("data.txt", JSON.stringify(records, null, 2), (err) => {
      if (err) {
        console.error("Erro ao escrever no arquivo:", err);
        return res.status(500).json({ error: "Erro ao escrever no arquivo." });
      }
      console.log("Registro atualizado com sucesso!");
      res.json(recordToUpdate);
    });
  });
});

// Rota para excluir um registro (DELETE)
app.delete("/delete", (req, res) => {
  const id = req.body.id; // Obtém o ID do corpo da requisição
  console.log("Excluindo registro com ID:", id);

  fs.readFile("data.txt", "utf8", (err, data) => {
    if (err) {
      console.error("Erro ao ler o arquivo:", err);
      return res.status(500).json({ error: "Erro ao ler o arquivo." });
    }
    let records = data ? JSON.parse(data) : [];
    records = records.filter((r) => r.id != id); // Remove o registro com o ID correspondente
    fs.writeFile("data.txt", JSON.stringify(records, null, 2), (err) => {
      if (err) {
        console.error("Erro ao escrever no arquivo:", err);
        return res.status(500).json({ error: "Erro ao escrever no arquivo." });
      }
      console.log("Registro excluído com sucesso!");
      res.json({ message: "Registro excluído com sucesso!" });
    });
  });
});

// Inicia o servidor na porta 3000
app.listen(3000, () => {
  console.log("Servidor rodando na porta 3000");
});
