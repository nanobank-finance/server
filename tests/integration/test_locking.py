from unittest.mock import Mock
from mockfirestore import MockFirestore
from src.firestore import lock_user, unlock_user, update_applicant_id

def test_lock_user_successfully():
    db = MockFirestore()
    user_ref = db.collection('users').document('test_user')
    user_ref.set({'locked': False})

    assert lock_user(user_ref) == True
    assert user_ref.get().to_dict()['locked'] == True

def test_unlock_user_successfully():
    db = MockFirestore()
    user_ref = db.collection('users').document('test_user')
    user_ref.set({'locked': True})

    assert unlock_user(user_ref) == True
    assert user_ref.get().to_dict()['locked'] == False
