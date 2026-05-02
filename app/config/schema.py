import uuid
from pydantic import BaseModel


class UserSchema(BaseModel):
    user_id: uuid.UUID
    query: str


class AgentSchema(BaseModel):
    user_id: uuid.UUID
    respones: str


class AgentConfig:
    model_name = "llama-3.3-70b-versatile"
    suppoet_model = "llama-3.1-8b-instant"
