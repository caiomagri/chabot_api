import os
import openai

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


class Bot:
    MAPPER_CALLER = {
        "chatgpt": "call_chatgpt",
        "chatterbot": "call_chatterbot",
    }

    def __init__(self):
        self.bot_type = os.getenv("CHATBOT_TYPE", "chatgpt")
        if self.bot_type == "chatgpt":
            self.api_key = os.getenv("CHATGPT_API_KEY")
            self.api_url = os.getenv("CHATGPT_API_URL")
            self.gpt_model = os.getenv("CHATGPT_MODEL")
            self.gpt_system_role = os.getenv("CHATGPT_SYTEM_ROLE", None)
        else:
            self.chatbot = ChatBot(
                os.getenv("CHATBOT_NAME", "Chatbot"),
                storage_adapter=os.getenv("CHATBOT_STORAGE_ADAPTER"),
                database_uri=os.getenv("CHATBOT_DATABASE_URI"),
            )
            self.trainer = ChatterBotCorpusTrainer(self.chatbot)
            self.trainer.train(
                "chatterbot.corpus.portuguese.greetings",
                "chatterbot.corpus.portuguese.conversations",
                "chatterbot.corpus.portuguese.suggestions",
            )

    def get_response(self, text):
        return getattr(self, self.MAPPER_CALLER[self.bot_type])(text)

    def call_chatterbot(self, text):
        return self.chatbot.get_response(text)

    def call_chatgpt(self, text):
        openai.api_key = self.api_key

        messages = [
            {"role": "user", "content": text},
        ]

        if self.gpt_system_role:
            messages.append(
                {
                    "role": "system",
                    "content": str(self.gpt_system_role),
                },
            )

        response = openai.ChatCompletion.create(
            model=self.gpt_model,
            messages=messages,
            max_tokens=int(os.getenv("CHATGPT_MAX_TOKENS", 400)),
        )
        return response["choices"][0]["message"]["content"]
