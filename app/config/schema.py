from dataclasses import dataclass
from pydantic import Field
from typing import List


@dataclass
class UserSchema:
    user_id: str = Field(str)
    query: str = Field(str)


@dataclass
class AgentSchema:
    respones: List[str] = Field(str)


@dataclass
class AgentConfig:
    model_name = "llama-3.3-70b-versatile"
    suppoet_model = "llama-3.1-8b-instant"
