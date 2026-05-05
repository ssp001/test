from app.core.agentabstract import AgentAbstract, AsyncGenerator
from app.config.schema import UserSchema, AgentSchema

from app.utils.custome import AiTimeoutError, AiUnavalabileError, LogicError


class AgentService:
    def __init__(self, client: AgentAbstract):
        self.client = client

    async def ai_respones(self, user: UserSchema) -> AsyncGenerator:
        try:
            async for chunk in self.client.run_agent(user):
                yield chunk
        except AiTimeoutError as error:
            raise ("sorry user request timeout") from error
        except AiUnavalabileError as error:
            raise (
                "sorry user request failiure ai unavalaivle for the moment") from error
        except LogicError as error:
            raise ("there is a lociv error in the server side")
