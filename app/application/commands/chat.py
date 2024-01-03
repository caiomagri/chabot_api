import re
import inject

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

from app.settings import Settings
from app.infrastructure.openai.api import ApiOpenaiClient

CONST_RESULT_PATTERN = r"<result>(.*?)</result>"


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

    def execute(self, text, recover_prompt):
        prompt = recover_prompt("default_system_prompt")
        messages = self.build_messages(text, prompt)
        return getattr(self, self.MAPPER_CALLER[self.bot_type])(messages)

    def call_chatterbot(self, prompt):
        return self.chatbot.get_response(prompt)

    def call_openai(self, messages) -> str:
        client = ApiOpenaiClient(self.settings)
        completion = client.execute_chat_completion(messages)
        content = completion["content"].strip()

        try:
            result = re.search(CONST_RESULT_PATTERN, content).group(1)
            if result and result == "BUSCA":
                message = "*Descrição*: Reservatório de água do radiador"
                message += "\n*Preço*: R$ 204,88"
                message += "\n*Marcar/Fabricante*: FIAT"
                message += "\n*Tabela de Aplicação*: Argo 2017/2021, Cronos 2018/2021"
                message += "\n*Compre agora*: https://pecapecas.com.br/produto/336205977-reservatorio-ex"

                return message

        except Exception as e:
            pass

        return content

    def build_messages(self, text, system_prompt):
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": text}]
        return messages
