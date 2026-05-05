from app.routers import routers
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST


REQUEST_COUNT = Counter('request_count', 'Total Request Count')


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    REQUEST_COUNT.inc()
    return {"message": "server is healthy to start"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


app.include_router(router=routers.router, prefix="/app/v1")
