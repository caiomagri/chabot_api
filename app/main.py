import inject
from fastapi import FastAPI

from app.models.payload import ChatbotPayload
from app.infrastructure.prompts import recover_prompt
from app.application.commands.chat import ChatBotCommand


app = FastAPI()

chatbot_command = inject.instance(ChatBotCommand)


@app.get("/health_check")
def health_check():
    return {"message": "alive"}


@app.post("/chatbot")
async def chatbot(
    payload: ChatbotPayload,
):
    response = chatbot_command.execute(payload.question, recover_prompt)
    return {
        "answer": str(response),
        "media_url": 'https://raw.githubusercontent.com/dianephan/flask_upload_photos/main/UPLOADS/DRAW_THE_OWL_MEME.png'
    }
