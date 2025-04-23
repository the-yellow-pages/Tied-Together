
def test_vehiclesdb(vehicles_db):
    """
    Test the VehiclesDB class.
    """
    db = vehicles_db
    
    # Test get_big_capacity method
    result = db.get_big_capacity(3000)
    assert isinstance(result, list), "Expected a list of vehicles"
    assert len(result) > 0, "Expected at least one vehicle with cubic capacity greater than 3000"