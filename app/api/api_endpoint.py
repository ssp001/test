from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.routers import routers


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
    return {"message": "server is healthy to start"}


app.include_router(router=routers.router, prefix="/app/v1")
