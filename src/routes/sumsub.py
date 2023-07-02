"""Sumsub Routes."""
from http.client import HTTPException
from fastapi import Depends
from fastapi import FastAPI
from typing import Self

from src.schemas import SuccessOrFailureResponse
from src.utils import RouterUtils
from src.sumsub import create_applicant, get_applicant_status, get_access_token
from src.firestore import db, update_applicant_id, lock_user

from fastapi import HTTPException
import time


class SumsubRouter():

    def __init__(self: Self, app: FastAPI) -> None:
        self.app = app

        # @app.get("/onboard/status", response_model=SuccessOrFailureResponse)
        # async def onboard_status(
        #     user: str = Depends(RouterUtils.get_user_token)
        # ) -> SuccessOrFailureResponse:
        #     """Query Firestore to see if the user has been onboarded yet

        #     Args:
        #         user (str): The user to submit the application for.

        #     Returns:
        #         SuccessOrFailureResponse: `success=True` when successful.
        #     """

        #     # check if user id is "locked" in firestore
        #     user_ref = db.collection('users').document(user)
        #     if not user_ref.locked:
        #         raise HTTPException(
        #             status_code=400,
        #             detail="Race condition averted; duplicate request is already in progress"
        #         )

        #     if user_doc.get('locked'):
        #         return SuccessOrFailureResponse(success=False, message="User is currently locked")

        #     # "lock" user id mapping to prevent race conditions
        #     lock_user(user_ref)

        #     try:
        #         # get applicant id corresponding to user from firestore
        #         applicant_id = user_ref.get('applicant_id')

        #         # if the applicant id does not exist, create a new one in sumsub
        #         # and store the id in firestore
        #         if not applicant_id:
        #             applicant_id = sumsub_api.create_applicant_id(user)
        #             update_applicant_id(user_ref, applicant_id)

        #         # query sumsub for the status of the applicant id
        #         status = sumsub_api.get_status(applicant_id)

        #         # Generate response based on status
        #         if status == "success":
        #             return SuccessOrFailureResponse(success=True)
        #         else:
        #             return SuccessOrFailureResponse(success=False)

        #     except Exception as e:
        #         return SuccessOrFailureResponse(success=False, message=str(e))

        #     finally:
        #         # Unlock user
        #         unlock_user(user_ref)

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
