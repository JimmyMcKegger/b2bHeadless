from fastapi import FastAPI
from utils.routes import router


app = FastAPI()
app.include_router(router)
