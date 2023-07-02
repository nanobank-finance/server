from tenacity import retry, wait_exponential, stop_after_attempt
from google.cloud import firestore
from typing import Any

db = firestore.Client()


@retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(5)
)
def lock_user(user_ref: Any) -> None:
    """
    Locks the user.

    Args:
        user_ref: The reference to the user document in Firestore.
    """
    user_ref.update({'locked': True})


@retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(5)
)
def unlock_user(user_ref: Any) -> Any:
    """
    Unlocks the user.

    Args:
        user_ref: The reference to the user document in Firestore.
    """
    user_ref.update({'locked': False})


@retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(5)
)
def update_applicant_id(user_ref: Any, applicant_id: str) -> None:
    """
    Updates the applicant ID in Firestore.

    Args:
        user_ref: The reference to the user document in Firestore.
        applicant_id: The applicant ID to store.
    """
    user_ref.update({'applicant_id': applicant_id})
