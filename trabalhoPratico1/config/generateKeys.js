// Importa as funções necessárias dos módulos 'crypto' e 'fs'
const { generateKeyPairSync } = require("crypto");
const fs = require("fs");

// Gera um par de chaves RSA (pública e privada)
const { publicKey, privateKey } = generateKeyPairSync("rsa", {
  modulusLength: 2048, // Tamanho da chave em bits (2048 é considerado seguro)
});

// Salva a chave pública em um arquivo
fs.writeFileSync(
  "public_key.pem", // Nome do arquivo para a chave pública
  publicKey.export({ type: "pkcs1", format: "pem" }) // Exporta no formato PEM (PKCS#1)
);

// Salva a chave privada em um arquivo
fs.writeFileSync(
  "private_key.pem", // Nome do arquivo para a chave privada
  privateKey.export({ type: "pkcs1", format: "pem" }) // Exporta no formato PEM (PKCS#1)
);

// Exibe uma mensagem no console confirmando que as chaves foram geradas e salvas
console.log(
  "Chaves RSA geradas e salvas como public_key.pem e private_key.pem"
);
