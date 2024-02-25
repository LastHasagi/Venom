const fs = require("fs");

function processJsonFile(inputFilePath, outputFilePath) {
  // Lê o arquivo JSON
  const rawData = fs.readFileSync(inputFilePath);
  const jsonData = JSON.parse(rawData);

  // Filtra e processa apenas os objetos com phoneUnformatted não nulo
  const processedData = jsonData
    .filter((item) => item.phoneUnformatted !== null)
    .map((item) => {
      // Verifica se phoneUnformatted existe e não é nulo
      const phoneNumber = item.phoneUnformatted
        ? item.phoneUnformatted.replace("+", "")
        : "";

      // Cria um novo objeto com as informações desejadas
      const newData = {
        phone: phoneNumber,
        key: item.key,
        value: item.value,
        title: item.title,
      };

      return newData;
    });

  // Cria um novo arquivo JSON com as informações processadas
  const outputData = JSON.stringify(processedData, null, 2);
  fs.writeFileSync(outputFilePath, outputData);

  console.log("Arquivo processado com sucesso!");
}

// Exemplo de uso
const inputFilePath = "./clientes.json";
const outputFilePath = "./prodNumbers.json";

processJsonFile(inputFilePath, outputFilePath);
