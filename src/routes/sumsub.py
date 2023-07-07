"""Sumsub Routes."""
from http.client import HTTPException
from fastapi import Depends
from fastapi import FastAPI
from typing import Self

from src.schemas import SuccessOrFailureResponse
from src.utils import RouterUtils
from src.sumsub import create_applicant, get_applicant_status, get_access_token
from src.firestore import db, update_applicant_id, lock_user, unlock_user

from fastapi import HTTPException
import time
import logging

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class SumsubRouter():

    def __init__(self: Self, app: FastAPI) -> None:
        self.app = app

        @app.get("/onboard/status", response_model=SuccessOrFailureResponse)
        async def onboard_status(
            user: str = Depends(RouterUtils.get_user_token)
        ) -> str:
            """Query Firestore to see if the user has been onboarded yet

            Only one request can be in progress at a time for a given user.
            This is verified by checking if the user id is "locked" in firestore.

            Args:
                user (str): The user to submit the application for.

            Returns:
                str: The user status
            """
            # check if user id is "locked" in firestore
            LOG.debug(f"Checking if user {user['uid']} is locked")
            user_ref = db.collection('users').document(user['uid'])
            doc = user_ref.get()
            if not doc.exists:
                LOG.debug(f"User {user['uid']} not found. Creating new user.")
                user_ref.set({'uid': user['uid'], 'locked': False}, merge=True)
                doc = user_ref.get()

            user_data = doc.to_dict()
            if user_data.get('locked', False):
                raise HTTPException(
                    status_code=400,
                    detail="Duplicate request is already in progress"
                )

            # "lock" user id mapping to prevent race conditions
            lock_user(user_ref)

            try:
                # get applicant id corresponding to user from firestore
                applicant_id = user_data.get('applicant_id')

                # if the applicant id does not exist,
                # create a new one in sumsub
                # and store the id in firestore
                if not applicant_id:
                    applicant_id = create_applicant(user, 'basic-kyc-level')
                    update_applicant_id(user_ref, applicant_id)

                # query sumsub for the status of the applicant id
                status = get_applicant_status(applicant_id)
                LOG.debug(f"Applicant {applicant_id} status: {status}")
                return status

            except Exception as e:
                LOG.exception(e)
                return SuccessOrFailureResponse(
                    success=False, message=type(e).__name__
                )

            finally:
                # Unlock user
                unlock_user(user_ref)

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
