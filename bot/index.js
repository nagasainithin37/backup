const exp = require("express");
const app = exp();
// const axios = require("axios");
app.use(exp.json());
const TelegramBot = require("node-telegram-bot-api");
// replace the value below with the Telegram token you receive from @BotFather
const token = "6530501862:AAHn2PpBLrAy-LgZJZFXz8OdoSRK62_-HJM";

// Create a bot that uses 'polling' to fetch new updates
const bot = new TelegramBot(token, { polling: true });

bot.onText(/\/signin$/, (msg, match) => {
  console.log(msg);
  const chatId = msg.chat.id;
  console.log(match);
  const resp = match[1];
  bot.sendMessage(chatId, "Your Id is " + chatId);
});

app.post("/send", async (req, res) => {
  body = req.body;
  // console.log(req.body);
  bot.sendMessage(body.chatId, "Your OTP is " + body.otp);
  res.send({ message: "success" });
});

app.listen(3100, () => {
  console.log("Server is running");
});
