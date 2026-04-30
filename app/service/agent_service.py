from core.agentabstract import AgentAbstract, AsyncGenerator
from config.schema import UserSchema


class AgentService:
    def __init__(self, client: AgentAbstract):
        self.client = client

    async def ai_respones(self, query) -> AsyncGenerator:
        async for chunk in self.client.run_agent(query):
            yield chunk
