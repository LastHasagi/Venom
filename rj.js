const venom = require("venom-bot");
const fs = require("fs");

venom
  .create({
    session: "RJ", 
  })
  .then((client) => sendMessages(client))
  .catch((err) => {
    console.log(err);
  });

const sendMessages = async (client) => {
  try {
    const phoneNumbers = JSON.parse(fs.readFileSync("./prodNumbersRJ.json"));
    const sentNumbers = JSON.parse(fs.readFileSync("./sentNumbersRJ.json"));
    for (const phoneNumber of phoneNumbers) {
      const alreadySentNumber = sentNumbers.find(
        (n) => n.phone === phoneNumber.phone
      );

      if (!alreadySentNumber) {
        await client
          .sendText(
            `${phoneNumber.phone}@c.us`,
            'Oioioi, Digu aqui ! viu, te mandei msg e vc nem notou !'
          )
          .then((result) => {
            console.log("Result: ", result); 
            console.log("Mensagem enviada para: ", phoneNumber.title);
          })
          .catch((err) => {
            console.error("Error when sending: ", err); 
          });

        sentNumbers.push(phoneNumber);
        fs.writeFileSync("sentNumbersRJ.json", JSON.stringify(sentNumbers));
      }
    }
  } catch (error) {
    console.error(`Error sending messages: ${error}`);
  }
};
