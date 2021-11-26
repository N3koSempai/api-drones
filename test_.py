from modules import battery, connect_db
import json
import unittest




class TestClass(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        self.test_data = {}
        self.test_data["serial"] = 'L0000'
        self.test_data["model"] = 'Lightweight'
        self.test_data["weigth"] =  500
        self.test_data["battery"] = 100
        self.test_data["state"] = 'IDLE'
        self.datajs = json.dumps(self.test_data, indent= 4)
        self.database = connect_db.db_connection()
        super(TestClass, self).__init__(*args, **kwargs)
        
    def test_battery_level(self):
        battery_levels = []
        for i in range(0, 101):
            battery_levels.append(str(i) + "%")
            
        battery_s = battery.battery_status() #instanciate the class in battery module
        status = battery_s.get_status() #take the actual status of the battery
        self.assertIn(status, battery_levels)

    def test_insert_drone(self): # for this test delete the db because duplication error with a Unique field inside the db
        
        self.database.initial_state() #create the database if not exist for the full test
        self.assertTrue(self.database.insert_drone(self.datajs))
    
    #def test_get_data(self): #is not posible run this test with the test_insert_drone . run the other fist and after this
    #   self.assertTrue(self.database.get_data(self.datajs))

    #def test_delete_drone(self): #not compatible for now with test_insert_drone
    #    self.assertTrue(self.database.delete(self.datajs))


    def 
if __name__ == "__main__":
    unittest.main()