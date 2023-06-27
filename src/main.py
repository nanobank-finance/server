"""Main."""
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from firebase_admin import credentials, initialize_app

import src.utils
from src.routes.application import LoanApplicationRouter
from src.routes.loan import LoanRouter
from src.routes.vouch import VouchRouter
from src.routes.sumsub import SumsubRouter

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
async def startup_firebase() -> None:
    """Initialize firebase app."""
    # firebase auth credentials
    load_dotenv(Path(os.environ['SECRETS_PATH'] + "/.env.nanobank"))
    initialize_app(
        credential=credentials.Certificate(
            os.environ['FIREBASE_CREDENTIALS_PATH']
        )
    )


@app.on_event("startup")
async def startup_feature_store() -> None:
    """Initialize feature store."""
    # feature store config
    src.utils.get_config()


@app.on_event("startup")
async def startup_router() -> None:
    """Add routes."""
    # add loan routes
    LoanApplicationRouter(app)
    LoanRouter(app)
    VouchRouter(app)
    SumsubRouter(app)


@app.on_event("startup")
async def startup_logger() -> None:
    """Initialize logger."""
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
    )
    logger.addHandler(handler)
