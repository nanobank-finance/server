"""Sumsub Routes."""
from fastapi import Depends
from fastapi import FastAPI
from typing import Self

from src.schemas import SuccessOrFailureResponse
from src.utils import RouterUtils
from src.sumsub import create_applicant, get_applicant_status, get_access_token


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
            pass

            # "lock" user id mapping to prevent race conditions
            pass

            # get applicant id corresponding to user from firestore
            pass

            # if the applicant id does not exist, create a new one in sumsub
            # and store the id in firestore
            pass

            # query sumsub for the status of the applicant id
            pass

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
