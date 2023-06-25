from fastapi import FastAPI

from app.setup_bot import Bot
from app.models.payload import ChatbotPayload

app = FastAPI()
bot = Bot()


@app.get("/health_check")
def health_check():
    return {"message": "alive"}


@app.post("/chabot")
async def chatbot(
    payload: ChatbotPayload,
):
    response = bot.get_response(payload.question)
    return {
        "answer": str(response),
    }
