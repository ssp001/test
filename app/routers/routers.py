from fastapi import APIRouter
from fastapi.responses import StreamingResponse


from app.src.agno_engine import AgnoClient
from app.service.agent_service import AgentService

import uuid

from typing_extensions import AsyncGenerator
from app.config.schema import UserSchema, AgentSchema

from fastapi import HTTPException

import json

router = APIRouter()

tutor_service = AgentService(client=AgnoClient())


@router.get("/")
def home():
    return {"message": "server is healthy to start"}


@router.post("/tutor_respones")
async def main(query: str) -> AsyncGenerator[AgentSchema, None]:
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

        return StreamingResponse(serrializer(), media_type="text/plain")
    except TimeoutError as error:
        raise HTTPException(status_code=504,
                            detail="Ai request time out sorry for this problem in the internal server") from error
    except TypeError as error:
        raise HTTPException(status_code=422,
                            detail="error occured while running input type is wrong sorry for interuption") from error
