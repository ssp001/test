from fastapi import APIRouter
from fastapi.responses import StreamingResponse


from app.src.agno_engine import AgnoClient
from app.service.agent_service import AgentService

from app.utils.custome import LogicError, AiTimeoutError, AiUnavalabileError
from app.utils.logger import _logger_method

import uuid

from typing_extensions import AsyncGenerator
from app.config.schema import UserSchema, AgentSchema

from fastapi import HTTPException
from fastapi import Request

from slowapi.util import get_remote_address
from slowapi import Limiter

import json

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
tutor_service = AgentService(client=AgnoClient())
logging = _logger_method(file_handeler="monitor/ai_endpoint")


@router.get("/")
def home():
    return {"message": "server is healthy to start"}


@router.post("/tutor_respones")
@limiter.limit("10/minute")
async def main(request: Request, query: str) -> AsyncGenerator[AgentSchema, None]:
    try:
        user_query = UserSchema(
            user_id=uuid.uuid4(),
            query=query
        )

        async def serrializer():
            full_respones = ""
            async for chunk in tutor_service.ai_respones(user=user_query):
                full_respones += chunk.respones
            yield json.dumps({
                "user_id": str(user_query.user_id),
                "respones": full_respones
            }) + "\n"
        logging.info(msg="ai respones has been fetched succesfully")
        return StreamingResponse(serrializer(), media_type="text/plain")
    except AiTimeoutError as error:
        raise HTTPException(status_code=504,
                            detail="Ai request time out sorry for this problem in the internal server😰") from error
    except LogicError as error:
        raise HTTPException(status_code=422,
                            detail="error occured while running input type is wrong sorry for interuption😩") from error
    except AiUnavalabileError as error:
        raise HTTPException(
            status_code=503, detail="service unavalavile for this moment sorry for this probelm😥")
