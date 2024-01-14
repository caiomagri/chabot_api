import re
import inject
import logging

from app.settings import Settings
from app.infrastructure.openai.api import ApiOpenaiClient
from app.infrastructure.search.api import ApiSearchClient

_logger = logging.getLogger(__name__)

CONST_RESULT_PATTERN = r"<RESULT>(.*?)</RESULT>"
CONST_ITEM_PATTERN = r"<ITEM>(.*?)</ITEM>"


class ChatBotCommand:
    MAPPER_CALLER = {
        "openai": "call_openai",
    }

    @inject.autoparams()
    def __init__(self, settings: Settings):
        self.settings = settings
        self.bot_type = self.settings.CHATBOT_TYPE

    def execute(self, text, recover_prompt):
        prompt = recover_prompt("default_system_prompt")
        messages = self.build_messages(text, prompt)
        return getattr(self, self.MAPPER_CALLER[self.bot_type])(messages)

    def call_openai(self, messages) -> str:
        client = ApiOpenaiClient(self.settings)
        completion = client.execute_chat_completion(messages)
        content = completion["content"].strip()

        try:
            result = re.search(CONST_RESULT_PATTERN, content)
            if result and result.group(1) == "BUSCA":
                search_client = ApiSearchClient(self.settings)
                item = re.search(CONST_ITEM_PATTERN, content)
                if item and item.group(1):
                    content = search_client.search(item.group(1))
        except Exception as e:
            _logger.error(f"Erro ao consultar Produto {str(e)}")
            content = "Tivemos um problema para fazer a busca. Por favor, tente novamente."

        return content

    def build_messages(self, text, system_prompt):
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": text}]
        return messages
