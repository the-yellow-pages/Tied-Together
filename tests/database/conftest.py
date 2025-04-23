import pytest
from unittest import mock
from database.Vehicles import VehiclesDB
from database.User import UsersDB

@pytest.fixture
def vehicles_db():
    db = VehiclesDB()
    original_connection = db.connection
    db.connection = mock.MagicMock(wraps=db.connection)
    db.cursor = mock.MagicMock(wraps=db.cursor)

    db.connection.commit = mock.MagicMock()
    
    yield db

    db.connection.rollback()
    db.connection = original_connection

@pytest.fixture
def user_db():
    db = UsersDB()

    original_connection = db.connection
    db.connection = mock.MagicMock(wraps=db.connection)
    db.cursor = mock.MagicMock(wraps=db.cursor)

    db.connection.commit = mock.MagicMock()
    
    yield db

    db.connection.rollback()
    db.connection = original_connection
    
