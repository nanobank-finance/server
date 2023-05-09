# Nano Swap Webserver

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/24893896-c8493f2f-581d-4fae-8148-3f49dca1ca42?action=collection%2Ffork&collection-url=entityId%3D24893896-c8493f2f-581d-4fae-8148-3f49dca1ca42%26entityType%3Dcollection%26workspaceId%3D52b14572-4c15-4e0d-8e65-5d035a3006f1)

## Setup:
`python3.11 pip install -r requirements.txt`

## Start the emulator and the web app:

Run: `export FIREBASE_AUTH_EMULATOR_HOST="localhost:9099"; uvicorn src.main:app --reload`

## Local API docs:
http://127.0.0.1:8000/docs#/ or http://127.0.0.1:8000/redoc


## Build, run tests, and run linter:

`nox --verbose`
To only run tests: `pytest --cov=bizlogic --log-cli-level=debug`  
