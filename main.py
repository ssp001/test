from fastapi import FastAPI
from app.api.api_endpoint import router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(name="AI Agent")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
