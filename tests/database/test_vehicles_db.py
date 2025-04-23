from database.Vehicles import VehiclesDB

def test_get_big_capacity(vehicles_db):
    """
    Test the VehiclesDB class.
    """
    db = vehicles_db
    
    # Test get_big_capacity method
    result = db.get_big_capacity(3000)
    assert isinstance(result, list), "Expected a list of vehicles"
    assert len(result) > 0, "Expected at least one vehicle with cubic capacity greater than 3000"
    
def test_get_filtered():
    """
    Test the VehiclesDB class.
    """
    db = VehiclesDB()
    result = db.get_filtered_cars()
    assert isinstance(result, list), "Expected a list of vehicles"
    assert len(result) > 0, "Expected at least one vehicle in the specified range"
    car = result[0]
    assert 'price' in car, "Expected vehicle to have a price"
    assert 'gross_amount' in car, "Expected vehicle to have a gross amount"
    # assert all(vehicle['gross_amount'] >= 1000 and vehicle['gross_amount'] <= 20000 for vehicle in result), "Expected all vehicles to be within the specified price range"