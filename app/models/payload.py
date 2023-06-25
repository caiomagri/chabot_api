from pydantic import BaseModel


class ChatbotPayload(BaseModel):
    question: str
