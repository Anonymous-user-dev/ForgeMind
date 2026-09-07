from fastapi import FastAPI
from app.executions.router import router


app = FastAPI()

app.include_router(router)