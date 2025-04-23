
def test_create_user(user_db):
    """
    Test the UserDB class.
    """
    db = user_db
    user_data = {
        'id': 1111,
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'johndoe'
    }
    res = db.create_user(user_data)
    assert res == 1111, "Expected user ID to be 1111"
    
def test_read_user(user_db):
    """
    Test the read_user method.
    """
    db = user_db
    assert db.read_user(1111) == None, "Expected user to be None"