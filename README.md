# Nano Swap Webserver

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/24893896-c8493f2f-581d-4fae-8148-3f49dca1ca42?action=collection%2Ffork&collection-url=entityId%3D24893896-c8493f2f-581d-4fae-8148-3f49dca1ca42%26entityType%3Dcollection%26workspaceId%3D52b14572-4c15-4e0d-8e65-5d035a3006f1)

## Setup:
`python3.11 pip install -r requirements.txt`

Add environment variables to `os.environ['SECRETS_PATH'] + "/.env.nanoswap"` (set the `SECRETS_PATH` environment variable as needed)

## Start the emulator and the web app:

Run: `uvicorn src.main:app --reload`

## Local API docs:
http://127.0.0.1:8000/docs#/ or http://127.0.0.1:8000/redoc


## Build, run tests, and run linter:

`nox --verbose`
To only run tests: `pytest --cov=bizlogic --log-cli-level=debug`  

## Gcloud Auth Issues

Note, this command may be needed to fix gcloud auth issues. Both server and firebase auth emulator should be shut down when the command is run before being brought back up.
```
gcloud auth activate-service-account --key-file=PATH_TO_YOUR_SERVICE_ACCOUNT_JSON
gcloud auth login
```

If that doesn't work, look for the token file (usually located at ~/.config/gcloud/application_default_credentials.json) and delete it, then try running your program again. This will force the auth library to reauthenticate and create a new token file.
```
rm ~/.config/gcloud/application_default_credentials.json
gcloud auth login
gcloud auth application-default login
gcloud auth activate-service-account --key-file=PATH_TO_YOUR_SERVICE_ACCOUNT_JSON
```

You could also try:
```
cp PATH_TO_YOUR_SERVICE_ACCOUNT_JSON ~/.config/gcloud/application_default_credentials.json
```
