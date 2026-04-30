from fastapi import FastAPI
from routers import routers

app = FastAPI()


app.include_router(router=routers.router, prefix="/app/v1")
