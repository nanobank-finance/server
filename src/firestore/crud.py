from fastapi import HTTPException
import time
import logging

from google.cloud import firestore
from google.cloud.firestore_v1.transaction import Transaction

from src.firestore import db
from src.sumsub import create_applicant, get_applicant_status

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def check_locked(uid: str) -> bool:
    """Checks if a user is locked in Firestore.

    If the user does not exist, a new user document is created.

    Args:
        uid (str): The user id to check.

    Returns:
        bool: True if the user is locked, False otherwise.
    """
    # Check if user id is "locked" in Firestore
    LOG.debug(f"Checking if user {uid} is locked")
    user_ref = db.collection('users').document(uid)
    doc = user_ref.get()
    if not doc.exists:
        LOG.debug(f"User {uid} not found. Creating new user.")
        user_ref.set({'uid': uid, 'locked': False}, merge=True)
        return False

    data = doc.to_dict()
    return data.get('locked', False)


@firestore.transactional
def check_and_lock_user(transaction: Transaction, uid: str) -> str:
    """Perform the transaction of checking and locking the user.

    This function will be called within a Firestore transaction and ensures that
    the operations of checking and locking the user are performed atomically.

    Args:
        transaction (Transaction): The Firestore transaction instance.
        uid (str): The external user id to associate to the sumsub applicant id

    Raises:
        HTTPException: If the user is already locked.

    Returns:
        str: The status of the user.
    """
    user_ref = db.collection('users').document(uid)

    snapshot = user_ref.get(transaction=transaction)
    if not snapshot.exists:
        LOG.debug(f"User {uid} not found. Creating new user.")
        transaction.set(user_ref, {'uid': uid, 'locked': False})

    data = snapshot.to_dict()

    if data.get('locked', False):
        # If user is already locked, raise an HTTPException
        raise HTTPException(
            status_code=400,
            detail="Duplicate request is already in progress"
        )

    # Lock user if it's not locked
    transaction.update(user_ref, {'locked': True})

    # get applicant id corresponding to user from firestore
    applicant_id = data.get('applicant_id')

    # if the applicant id does not exist,
    # create a new one in sumsub
    # and store the id in firestore
    if not applicant_id:
        applicant_id = create_applicant(uid, 'basic-kyc-level')
        transaction.update(user_ref, {'applicant_id': applicant_id})

    # query sumsub for the status of the applicant id
    status = get_applicant_status(applicant_id)
    LOG.debug(f"Applicant {applicant_id} status: {status}")

    # Unlock user
    transaction.update(user_ref, {'locked': False})

    return status
