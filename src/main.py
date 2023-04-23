from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials, initialize_app
from dotenv import load_dotenv
from pathlib import Path
import os
import src.utils
from src.routes.loan import LoanRouter
from src.routes.application import LoanApplicationRouter
from src.routes.vouch import VouchRouter
import logging

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_firebase():
    # firebase auth credentials
    load_dotenv(Path(os.environ['SECRETS_PATH']+"/.env.nanobank"))
    initialize_app(credential=credentials.Certificate(os.environ['FIREBASE_CREDENTIALS_PATH']))


@app.on_event("startup")
async def startup_feature_store():
    # feature store config
    config = src.utils.get_config()


@app.on_event("startup")
async def startup_router():
    # add loan routes
    LoanApplicationRouter(app)
    LoanRouter(app)
    VouchRouter(app)

@app.on_event("startup")
async def startup_logger():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
