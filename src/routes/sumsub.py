"""Sumsub Routes."""
from http.client import HTTPException
from fastapi import Depends
from fastapi import FastAPI
from typing import Self

from src.schemas import SuccessOrFailureResponse, SumsubApplicantStatus
from src.utils import RouterUtils
from src.sumsub import create_applicant, get_applicant_status, get_access_token
from src.firestore import db
from src.firestore.crud import check_locked, check_and_lock_user

from google.cloud import firestore
from google.cloud.firestore_v1.transaction import Transaction

from fastapi import HTTPException
import time
import logging

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class SumsubRouter():

    def __init__(self: Self, app: FastAPI) -> None:
        self.app = app

        @app.get("/onboard/status", response_model=SumsubApplicantStatus)
        async def onboard_status(
            user: str = Depends(RouterUtils.get_user_token)
        ) -> str:
            """Query Firestore to see if the user has been onboarded yet.

            Only one request can be in progress at a time for a given user.
            This is verified by checking if the user id is "locked" in firestore.

            Args:
                user (str): The user to submit the application for.

            Returns:
                str: The user status
            """
            # Check if the user is locked
            if check_locked(user['uid']):
                raise HTTPException(
                    status_code=400,
                    detail="Duplicate request is already in progress"
                )

            # Initialize a Firestore transaction
            transaction = db.transaction()

            # Check and lock the user in the transaction
            try:
                return check_and_lock_user(transaction, user['uid'])
            except Exception as e:
                LOG.exception(e)
                transaction.rollback()
                raise HTTPException(status_code=400, detail=str(e))

        @app.post("/onboard/start", response_model=SuccessOrFailureResponse)
        async def start_onboarding(
            user: str = Depends(RouterUtils.get_user_token)
        ) -> SuccessOrFailureResponse:
            """Start the onboarding process.

             - Create a KYC applicant
             - Store the Auth user ID with the KYC applicant ID

            Args:
                user (str): The user to submit the application for.

            Returns:
                SuccessOrFailureResponse: `success=True` when successful.
            """
            pass
