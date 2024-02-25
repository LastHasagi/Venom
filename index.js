const venom = require("venom-bot");
const fs = require("fs");

venom
  .create({
    session: "Advocacia BSX", 
  })
  .then((client) => sendMessages(client))
  .catch((err) => {
    console.log(err);
  });

const sendMessages = async (client) => {
  try {
    const phoneNumbers = JSON.parse(fs.readFileSync("./prodNumbers.json"));
    const sentNumbers = JSON.parse(fs.readFileSync("./sentNumbers.json"));
    for (const phoneNumber of phoneNumbers) {
      const alreadySentNumber = sentNumbers.find(
        (n) => n.phone === phoneNumber.phone
      );

      if (!alreadySentNumber) {
        await client
          .sendImage(
            `${phoneNumber.phone}@c.us`,
            './folheto.jpeg',
            'folheto',
            "Somos a BSX Soluções financeiras ! Temos tudo o que sua empresa precisa no quesito informações ! Entre em contato conosco e saiba mais ou acessa nosso site: https://grupobsx.com.br/ !"
          )
          .then((result) => {
            console.log("Result: ", result); 
            console.log("Mensagem enviada para: ", phoneNumber.title);
          })
          .catch((err) => {
            console.error("Error when sending: ", err); 
          });

        sentNumbers.push(phoneNumber);
        fs.writeFileSync("sentNumbers.json", JSON.stringify(sentNumbers));
      }
    }
  } catch (error) {
    console.error(`Error sending messages: ${error}`);
  }
};
