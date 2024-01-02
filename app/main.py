import inject
from fastapi import FastAPI

from app.models.payload import ChatbotPayload
from app.application.commands.chat import ChatBotCommand


app = FastAPI()

chatbot_command = inject.instance(ChatBotCommand)


@app.get("/health_check")
def health_check():
    return {"message": "alive"}


@app.post("/chabot")
async def chatbot(
    payload: ChatbotPayload,
):
    response = chatbot_command.execute(payload.question)
    return {
        "answer": str(response),
    }
