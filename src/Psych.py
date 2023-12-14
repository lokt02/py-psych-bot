import configparser

import openai
import telebot
from openai import OpenAI
from src.Logger import log_info, log_init, log_error, log_debug

global_config = configparser.ConfigParser()
global_config.read("config.ini")
openai.api_key = global_config["OpenAI"]["api_key"]
commandList = ["/help"]

class Psych:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")

        self.bot = telebot.TeleBot(config["Telegram"]["token"])

        with open("start_prompt.txt", encoding='utf-8') as f:
            self.start_prompt = f.read()

        self.client = OpenAI(
            api_key=config["OpenAI"]["api_key"]
        )

        self.messages = {
            -1: [{"role": "assistant", "content": self.start_prompt}]
        }

        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            log_debug("handling message: " + message.text)
            if message.chat.id in self.messages.keys():
                self.messages[message.chat.id].append({"role": "user", "content": message.text})
            else:
                self.messages[message.chat.id] = [
                    self.messages[-1],
                    {"role": "user", "content": message.text}
                ]
            completion = openai.chat.completions.create(model='gpt-3.5-turbo', messages=self.messages[message.chat.id])
            reply = completion.choices[0].message.content
            log_info(f"ChatGPT: {reply}")
            self.bot.send_message(message.chat.id, reply)
            self.messages[message.chat.id].append({"role": "assistant", "content": str(reply)})


    def run(self):
        self.bot.infinity_polling()