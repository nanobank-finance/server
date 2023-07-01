"""Sumsub Routes."""
from http.client import HTTPException
from fastapi import Depends
from fastapi import FastAPI
from typing import Self

from google.cloud import firestore

from src.schemas import SuccessOrFailureResponse
from src.utils import RouterUtils
from src.sumsub import create_applicant, get_applicant_status, get_access_token

db = firestore.Client()

class SumsubRouter():

    def __init__(self: Self, app: FastAPI) -> None:
        self.app = app

        @app.get("/onboard/status", response_model=SuccessOrFailureResponse)
        async def onboard_status(
            user: str = Depends(RouterUtils.get_user_token)
        ) -> SuccessOrFailureResponse:
            """Query Firestore to see if the user has been onboarded yet

            Args:
                user (str): The user to submit the application for.

            Returns:
                SuccessOrFailureResponse: `success=True` when successful.
            """

            # check if user id is "locked" in firestore
            user_ref = db.collection('users').document(user)
            user_doc = user_ref.get()
            if not user_doc.exists or user_doc.get('locked'):
                raise HTTPException(status_code=400, detail="User is locked or does not exist")

            # "lock" user id mapping to prevent race conditions
            user_ref.update({'locked': True})

            # get applicant id corresponding to user from firestore
            applicant_id = user_doc.get('applicant_id')

            # if the applicant id does not exist, create a new one in sumsub
            # and store the id in firestore
            if not applicant_id:
                applicant_id = create_applicant(user)
                user_ref.update({'applicant_id': applicant_id})

            # query sumsub for the status of the applicant id
            status = get_applicant_status(applicant_id)

            # Unlock user
            user_ref.update({'locked': False})

            return status

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
