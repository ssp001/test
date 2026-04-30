from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from service.agent_service import AgentService
from core.agentabstract import AgnoClient

import uuid

from typing_extensions import AsyncGenerator
from config.schema import UserSchema

from fastapi import HTTPException


router = APIRouter()

tutor_service = AgentService(client=AgnoClient())


@router.get("/")
def home():
    return {"message": "good to start"}


@router.post("/tutor_respones")
async def main(query: str) -> AsyncGenerator:
    try:
        user = UserSchema(
            user_id=uuid.uuid4(),
            query=query
        )
        return StreamingResponse(tutor_service.ai_respones(query=user.query), media_type="text/plain")
    except TimeoutError as error:
        raise HTTPException(status_code=504,
                            detail="Ai request time out sorry for this problem in the internal server") from error
    except TypeError as error:
        raise HTTPException(status_code=422,
                            detail=" error occured while running input type is wrong sorry for interuption") from error
