const express = require("express");
const fs = require("fs");
const app = express();

app.use(express.json());

app.get("/", (req, res) => {
  const name = req.query.name;
  fs.readFile("data.txt", "utf8", (err, data) => {
    if (err) return res.status(500).json({ error: "Erro ao ler o arquivo" });
    const records = JSON.parse(data);
    const record = records.find((record) => record.name === name);
    if (record) {
      res.json(record);
    } else {
      res.json({ error: "data not found" });
    }
  });
});

app.post("/", (req, res) => {
  const record = req.body;
  fs.readFile("data.txt", "utf8", (err, data) => {
    let records = [];
    if (!err && data) records = JSON.parse(data);
    records.push(record);
    fs.writeFile("data.txt", JSON.stringify(records, null, 2), (err) => {
      if (err)
        return res.status(500).json({ error: "Erro ao salvar o arquivo" });
      res.json(record);
    });
  });
});

app.put("/", (req, res) => {
  const updatedRecord = req.body;
  fs.readFile("data.txt", "utf8", (err, data) => {
    if (err) return res.status(500).json({ error: "Erro ao ler o arquivo" });
    let records = JSON.parse(data);
    records = records.map((record) =>
      record.name === updatedRecord.name
        ? { ...record, email: updatedRecord.email }
        : record
    );
    fs.writeFile("data.txt", JSON.stringify(records, null, 2), (err) => {
      if (err)
        return res.status(500).json({ error: "Erro ao salvar o arquivo" });
      res.json(updatedRecord);
    });
  });
});

app.delete("/", (req, res) => {
  const recordToDelete = req.body;
  fs.readFile("data.txt", "utf8", (err, data) => {
    if (err) return res.status(500).json({ error: "Erro ao ler o arquivo" });
    let records = JSON.parse(data);
    records = records.filter((record) => record.name !== recordToDelete.name);
    fs.writeFile("data.txt", JSON.stringify(records, null, 2), (err) => {
      if (err)
        return res.status(500).json({ error: "Erro ao salvar o arquivo" });
      res.json(recordToDelete);
    });
  });
});

app.listen(3000, () => {
  console.log("Servidor rodando na porta 3000");
});
