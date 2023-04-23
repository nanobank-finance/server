from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials, initialize_app
from dotenv import load_dotenv
from pathlib import Path
import os
import src.utils
from src.routes.loan import LoanRouter

app = FastAPI()

# class Server():

#     @staticmethod
#     def startup():
#         # server setup
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

# firebase auth credentials
load_dotenv(Path(os.environ['SECRETS_PATH']+"/.env.nanobank"))
initialize_app(credential=credentials.Certificate(os.environ['FIREBASE_CREDENTIALS_PATH']))

# feature store config
config = src.utils.get_config()

# add loan routes
LoanRouter(app)

# Server.startup()
