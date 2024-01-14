import requests
from urllib.parse import quote

from langchain import OpenAI
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

from babel.numbers import format_currency

from app.settings import Settings
from app.infrastructure.prompts import recover_prompt


class ApiSearchClient:
    def __init__(self, settings: Settings):
        self.__settings = settings

    def search(self, text):
        if self.__settings.ECOMMERCE_SEARCH_ENGINE == "llm":
            return self._search_with_llm(text)

        return self._search_with_api(text)

    def _search_with_api(self, text):
        headers = {
            "Secret-key": self.__settings.ECOMMERCE_SECRET_KEY
        }

        base_url = f"{self.__settings.BASE_ECOMMERCE_URL}/search/product/api"
        params = {"query": text}
        response = requests.get(base_url, params=params, headers=headers)

        if response.status_code == 200:
            return self._build_api_response(response.json(), text)

        raise Exception(f"Erro ao consultar API de busca de produtos: {response.status_code}- {response.text}")

    def _format_money(self, number):
        return format_currency(number, 'BRL', locale='pt_BR')

    def _build_api_response(self, response, text):
        response_content = ""
        if not response["data"]:
            return f"Nenhum produto encontrado com a busca realizada: *{text}*.\n Tente fornercer mais informações sobre o produto ou veículo para que possamos te ajudar.\nex: *Pastilha de freio dianteira para o veículo Fiat Uno 2010*\n *Peças para o veículo Fiat Uno 2010*"

        for item in response["data"][0:1]:
            response_content += f"*Código:* {item['default_code']}\n"
            response_content += f"*Nome:* {item['name']}\n"
            response_content += f"*Preço:* {self._format_money(item['list_price'])}\n"
            response_content += f"*Marca:* {item['brand_producer']}\n"
            response_content += f"*Peças similares:* {item['similar_parts']}\n"
            response_content += f"*Tabela de aplicação:* {item['application_table']}\n"
            response_content += f"*Link:* {item['url']}\n"
            response_content += "\n"

        if len(response["data"]) > 1:
            response_content += f"Encontramos *{len(response['data'])}* produtos com a busca realizada: *{text}*.\n"
            response_content += f"Para ver todos os produtos, acesse o link abaixo:\n{'https://pecastecauto.com.br'}/shop?search={quote(text)}"

        return response_content

    def _search_with_llm(self, text):
        database = SQLDatabase.from_uri(
            self.__settings.DATABASE_ECOMMERCE_URI,
            include_tables=["product_template"]
        )
        llm = OpenAI(
            temperature=0,
            openai_api_key=self.__settings.OPENAI_TOKEN,
            max_tokens=1000
        )

        db_chain = SQLDatabaseChain.from_llm(
            llm, database
        )

        query = self._build_query(text)
        response = db_chain.run(query)
        return response

    def _build_query(self, text):
        prompt = recover_prompt("default_prompt_search")
        query = prompt.format(question=text, base_ecom_url=self.__settings.BASE_ECOMMERCE_URL)
        return query
