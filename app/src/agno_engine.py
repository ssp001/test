

import os

from app.core.agentabstract import AgentAbstract
from app.config.schema import AgentConfig, UserSchema, AgentSchema

from typing import AsyncGenerator
from app.utils.logger import _logger_method
from app.utils.custome import AiTimeoutError, LogicError, AiUnavalabileError

from pyresilience import resilient, RetryConfig, CircuitBreakerConfig, TimeoutConfig

from dotenv import load_dotenv

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.groq import Groq

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.tools.memory import MemoryTools
from agno.exceptions import AgnoError

logger = _logger_method(file_handeler="app/monitor/agno_core.log")
load_dotenv()


@resilient(
    retry=RetryConfig(max_attempts=5, delay=5.9),
    circuit_breaker=CircuitBreakerConfig(
        failure_threshold=5, recovery_timeout=50),
    timeout=TimeoutConfig(seconds=20, per_attempt=True)
)
class AgnoClient(AgentAbstract):
    """
    Agno client main logic
    ```Args:List[str] = query ```
    retrun:->```AsyncGenerator```
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
                   ],
            stream=True,
            description="You are a patient tutor. Track student progress in memory and explain step-by-step.",
        )
        logger.info("agent has incilized succsfully")

    async def run_agent(self, user: UserSchema) -> AsyncGenerator[AgentSchema, None]:
        try:
            async for chunk in self.cleint.arun(input=user.query, stream=True):
                logger.debug("agent query runing")
                yield AgentSchema(
                    user_id=user.user_id,
                    respones=chunk.content
                )

        except AgnoError as error:
            logger.exception(
                f"sorry an exception occured{str(error)}")
            raise AiUnavalabileError(
                "an error occure while runtime") from error

        except TimeoutError as error:
            logger.exception(
                "sorry agent rech timeout server is in high pressser")
            raise AiTimeoutError("ai request time out sorry") from error

        except AttributeError as error:
            logger.exception(
                f"sorry an exception occured{str(error)}")
            raise LogicError("an error occure while runtime") from error
