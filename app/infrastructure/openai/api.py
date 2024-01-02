import logging
from openai import OpenAI

from app.settings import Settings
from app.application.gateways.client.ai_client import AIApiClient


class ApiOpenaiClient(AIApiClient):
    def __init__(self, settings: Settings):
        self.__settings = settings
        self.client = OpenAI(
            api_key=settings.OPENAI_TOKEN,
        )

    def _get_options(self, options):
        default_options = {
            "temperature": float(self.__settings.OPENAI_TEMPERATURE),
            "top_p": float(self.__settings.OPENAI_TOP_P),
            "frequency_penalty": float(
                self.__settings.OPENAI_FREQUENCY_PENALTY
            ),
            "presence_penalty": float(self.__settings.OPENAI_PRESENCE_PENALTY),
            "max_tokens": int(self.__settings.OPENAI_MAX_TOKENS),
            "timeout": int(self.__settings.OPENAI_TIMEOUT),
            "model": self.__settings.OPENAI_CHAT_MODEL,
        }

        if not options:
            options = {}

        default_options.update(options)
        return default_options

    def _prepare_response(self, prompt_response, get_from_message=False):
        response = {
            "usage": {
                "completion_tokens": prompt_response.usage.completion_tokens,
                "prompt_tokens": prompt_response.usage.prompt_tokens,
                "total_tokens": prompt_response.usage.total_tokens,
            }
        }

        if prompt_response.choices:
            logging.info(prompt_response.choices)
            if get_from_message:
                response["content"] = prompt_response.choices[
                    0
                ].message.content
            else:
                response["content"] = prompt_response.choices[0].text
        return response

    def execute_chat_completion(self, prompt, options=None):
        options = self._get_options(options)

        options["messages"] = [{"role": "user", "content": prompt}]

        options["stop"] = [" User:", " Assistant:"]

        return self._prepare_response(
            self.client.chat.completions.create(**options), True
        )
