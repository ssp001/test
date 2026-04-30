from abc import (
    ABC,
    abstractmethod
)

from config.schema import UserSchema, AgentConfig

import os


from typing import AsyncGenerator
from utils.logger import _logger_method
from pyresilience import resilient, RetryConfig, CircuitBreakerConfig, TimeoutConfig

from dotenv import load_dotenv

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.groq import Groq

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.tools.memory import MemoryTools
from agno.tools.reasoning import ReasoningTools
from agno.exceptions import AgnoError

logger = _logger_method(file_handeler="app/monitor/agno_core.log")
load_dotenv()


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
    ) -> AsyncGenerator:

        pass


@resilient(
    retry=RetryConfig(max_attempts=5, delay=5.9),
    circuit_breaker=CircuitBreakerConfig(
        failure_threshold=5, recovery_timeout=50),
    timeout=TimeoutConfig(seconds=7, per_attempt=12)
)
class AgnoClient(AgentAbstract):
    """
    Agno client main logic
    ```Args:List[str] = query ```
    retrun->```AsyncGenerator```
    """

    def __init__(self):
        self.support = AgentConfig.suppoet_model
        self.db = SqliteDb(db_file="tmp/agno.db")
        self.cleint = Agent(
            model=Groq(id=AgentConfig.model_name,
                       api_key=os.getenv("GROQ_API_KEY")),
            fallback_models=[Groq(id=self.support)],
            tools=[DuckDuckGoTools(timeout=15),
                   MemoryTools(db=self.db),
                   ReasoningTools(add_instructions=True),
                   ],
            stream=True,
            description="You are a patient tutor. Track student progress in memory and explain step-by-step.",

        )
        logger.info("agent has incilized succsfully")

    async def run_agent(self, query: str) -> AsyncGenerator:
        try:
            async for chunk in self.cleint.arun(query, stream=True):
                logger.debug("agent query runing")
                yield chunk.content

        except AgnoError as error:
            logger.exception(
                f"sorry an exception occured{str(error)}")
            raise RuntimeError("an error occure while runtime") from error

        except TimeoutError as error:
            logger.exception(
                "sorry agent rech timeout server is in high pressser")
            raise RuntimeError("ai request time out sorry") from error

        except AttributeError as error:
            logger.exception(
                f"sorry an exception occured{str(error)}")
            raise RuntimeError("an error occure while runtime") from error
