import inject

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

from app.settings import Settings
from app.infrastructure.openai.api import ApiOpenaiClient


class ChatBotCommand:
    MAPPER_CALLER = {
        "openai": "call_openai",
        "chatterbot": "call_chatterbot",
    }

    @inject.autoparams()
    def __init__(self, settings: Settings):
        self.settings = settings
        self.bot_type = self.settings.CHATBOT_TYPE

        if self.bot_type == "chatterbot":
            self.chatbot = ChatBot(
                self.settings.CHATBOT_NAME,
                storage_adapter=self.settings.CHATBOT_STORAGE_ADAPTER,
                database_uri=self.settings.CHATBOT_DATABASE_URI,
            )
            self.trainer = ChatterBotCorpusTrainer(self.chatbot)
            self.trainer.train(
                "chatterbot.corpus.portuguese.greetings",
                "chatterbot.corpus.portuguese.conversations",
                "chatterbot.corpus.portuguese.suggestions",
            )

    def execute(self, text):
        return getattr(self, self.MAPPER_CALLER[self.bot_type])(text)

    def call_chatterbot(self, text):
        return self.chatbot.get_response(text)

    def call_openai(self, prompt) -> str:
        client = ApiOpenaiClient(self.settings)
        completion = client.execute_chat_completion(prompt)
        content = completion["content"].strip()
        return content
