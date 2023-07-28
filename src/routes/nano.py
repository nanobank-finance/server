from pydantic import BaseModel
from fastapi import Depends, HTTPException
from src.schemas import NanoAddressResponse
from src.utils import RouterUtils
from src.firestore import db
from src.firestore.crud import check_locked, check_and_lock_user
from nanohelp.wallet import WalletManager
from google.cloud import secretmanager


class NanoRouter():
    def __init__(self: Self, app: FastAPI) -> None:
        """Add routes for loans.

        Args:
            app (FastAPI): Routes will be added to this app.
        """
        # ipfsclient = Ipfs()
        # loan_reader = LoanReader(ipfsclient)

        # Initialize your WalletManager and Secret Manager client
        wallet_manager = WalletManager(node_address)
        secret_manager_client = secretmanager.SecretManagerServiceClient()


        def store_private_key_in_secret_store(user: str, private_key: str):
            """
            This method abstracts the process of storing a user's private key in Google Secret Manager.
            """
            # Set the name of the secret based on the user
            secret_name = f"user-{user}-private-key"

            # Create a new secret version
            secret = secret_manager_client.secret_version_path('your-project-id', secret_name, 'latest')
            secret_payload = {'text': private_key}

            # Add the secret version
            secret_manager_client.add_secret_version_with_rotation(
                parent=secret, payload=secret_payload,
                rotation_schedule=secretmanager.types.RotationSchedule(
                    next_rotation_time={'seconds': int(time.time() + 60 * 60 * 24 * 30)}  # rotate every 30 days
                )
            )


        def create_nano_wallet(user: str):
            """
            This method abstracts the process of creating a new nano wallet for the user.
            """
            wallet_id, account_address, private_key = wallet_manager.create_wallet()

            # Store the private key in Google Secret Manager
            store_private_key_in_secret_store(user, private_key)

            return account_address


        @app.get("/wallet/deposit", response_model=NanoAddressResponse)
        async def get_deposit_address(user: str = Depends(RouterUtils.get_user_token)) -> NanoAddressResponse:
            """Fetch the nano_address for the given user from Firestore. 
            If it does not exist, create a new wallet, save the address, and return the new address.

            Args:
                user (str): The user to fetch the nano_address for.

            Returns:
                NanoAddressResponse: The nano_address for the user.
            """
            user_ref = db.collection('users').document(user)
            doc = user_ref.get()

            if not doc.exists:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )

            user_data = doc.to_dict()
            nano_address = user_data.get('nano_address')

            # If nano_address does not exist, create a new wallet, save the address, and update nano_address
            if nano_address is None:
                nano_address = create_nano_wallet(user)
                user_data['nano_address'] = nano_address
                user_ref.set(user_data)

            return NanoAddressResponse(nano_address=nano_address)
