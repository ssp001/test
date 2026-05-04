
from fastapi.testclient import TestClient

from app.config.schema import UserSchema
from app.api.api_endpoint import app

from dotenv import load_dotenv
from typing_extensions import AsyncGenerator

import pytest

import os

# configuration
client = TestClient(app=app)
load_dotenv()


#######################################
# api endpoint status code check
#######################################


def test_tutor_endpoint_status_code() -> int:
    respones = client.post(
        url=os.getenv("URL"),
        params={"query": "hellow"}
    )
    assert respones.status_code == 200

#######################################
# api endpoint query code check
#######################################


@pytest.mark.asyncio
async def test_tutor_endpoint_query_test():
    chunk = []

    with client.stream(
        "POST",
        os.getenv("URL"),
        params={"query": "hello"}
    ) as response:
        for text in response.iter_text():
            chunk.append(text)

    assert len(chunk) > 0
