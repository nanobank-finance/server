import pytest
from unittest.mock import Mock
from src.firestore import lock_user, unlock_user, update_applicant_id

def test_lock_user():
    user_ref = Mock()  # Create a mock user_ref
    lock_user(user_ref)  # Call the function with the mock
    # Assert that the mock's update method was called with the expected arguments
    user_ref.update.assert_called_once_with({'locked': True})

def test_unlock_user():
    user_ref = Mock()  # Create a mock user_ref
    unlock_user(user_ref)  # Call the function with the mock
    # Assert that the mock's update method was called with the expected arguments
    user_ref.update.assert_called_once_with({'locked': False})

def test_update_applicant_id():
    user_ref = Mock()  # Create a mock user_ref
    update_applicant_id(user_ref, "test_applicant_id")  # Call the function with the mock
    # Assert that the mock's update method was called with the expected arguments
    user_ref.update.assert_called_once_with({'applicant_id': 'test_applicant_id'})
