from fastapi import FastAPI
from utils.routes import router
from utils.log import logging

app = FastAPI()
app.include_router(router)
logger = logging.getLogger(__name__)
