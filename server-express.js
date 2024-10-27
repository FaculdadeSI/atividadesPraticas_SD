const express = require("express");
const fs = require("fs");
const path = require("path");
const app = express();

// Middleware para servir arquivos estáticos
app.use(express.static(path.join(__dirname))); // Isso vai servir todos os arquivos na raiz do projeto
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
  const record = req.body;
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

// Rota para buscar um registro
app.get("/query", (req, res) => {
  const name = req.query.name;
  console.log("Buscando registro por nome:", name);

  fs.readFile("data.txt", "utf8", (err, data) => {
    if (err) {
      console.error("Erro ao ler o arquivo:", err);
      return res.status(500).json({ error: "Erro ao ler o arquivo." });
    }
    const records = data ? JSON.parse(data) : [];
    const record = records.find((r) => r.name === name);
    if (record) {
      return res.json(record);
    }
    return res.status(404).json({ error: "data not found" });
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
    records = records.map((r) =>
      r.name === recordToUpdate.name ? recordToUpdate : r
    );
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

// Rota para modificar um registro (PATCH)
app.patch("/modify", (req, res) => {
  const recordToModify = req.body;
  console.log("Modificando registro:", recordToModify);

  fs.readFile("data.txt", "utf8", (err, data) => {
    if (err) {
      console.error("Erro ao ler o arquivo:", err);
      return res.status(500).json({ error: "Erro ao ler o arquivo." });
    }
    let records = data ? JSON.parse(data) : [];
    records = records.map((r) => {
      if (r.name === recordToModify.name) {
        return { ...r, ...recordToModify };
      }
      return r;
    });
    fs.writeFile("data.txt", JSON.stringify(records, null, 2), (err) => {
      if (err) {
        console.error("Erro ao escrever no arquivo:", err);
        return res.status(500).json({ error: "Erro ao escrever no arquivo." });
      }
      console.log("Registro modificado com sucesso!");
      res.json(recordToModify);
    });
  });
});

// Rota para excluir um registro (DELETE)
app.delete("/delete", (req, res) => {
  const recordToDelete = req.body;
  console.log("Excluindo registro:", recordToDelete);

  fs.readFile("data.txt", "utf8", (err, data) => {
    if (err) {
      console.error("Erro ao ler o arquivo:", err);
      return res.status(500).json({ error: "Erro ao ler o arquivo." });
    }
    let records = data ? JSON.parse(data) : [];
    records = records.filter((r) => r.name !== recordToDelete.name);
    fs.writeFile("data.txt", JSON.stringify(records, null, 2), (err) => {
      if (err) {
        console.error("Erro ao escrever no arquivo:", err);
        return res.status(500).json({ error: "Erro ao escrever no arquivo." });
      }
      console.log("Registro excluído com sucesso!");
      res.json(recordToDelete);
    });
  });
});

// Endpoint OPTIONS para retornar métodos permitidos
// O método OPTIONS não precisa ser implementado manualmente no Express,
// pois o framework automaticamente responde com os métodos permitidos
// com base nas rotas definidas. Quando uma requisição OPTIONS é
// recebida, o Express verifica as rotas disponíveis e retorna
// os métodos adequados automaticamente.

app.listen(3000, () => {
  console.log("Servidor rodando na porta 3000");
});
