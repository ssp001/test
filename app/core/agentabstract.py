from abc import (
    ABC,
    abstractmethod
)

from app.config.schema import UserSchema, AgentSchema

import os


from typing import AsyncGenerator


class AgentAbstract(
    ABC
):
    """
    Abstraction point for ai bridge
    Args: query:str
    return:None
    """
    @abstractmethod
    async def run_agent(
        query: UserSchema
    ) -> AsyncGenerator[AgentSchema, None]:

        pass
