from app.core.agentabstract import AgentAbstract, AsyncGenerator
from app.config.schema import UserSchema, AgentSchema


from fastapi import HTTPException
import json


class AgentService:
    def __init__(self, client: AgentAbstract):
        self.client = client

    async def ai_respones(self, user: UserSchema) -> AsyncGenerator:
        try:
            async for chunk in self.client.run_agent(user):
                yield chunk
        except TimeoutError as error:
            raise RuntimeError("sorry user request timeout") from error
        except HTTPException as error:
            raise RuntimeError("sorry user request failiure") from error
