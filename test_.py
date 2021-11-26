from modules import battery, connect_db
import json
import unittest




class TestClass(unittest.TestCase):
    def test_battery_level(self):
        battery_levels = []
        for i in range(0, 101):
            battery_levels.append(str(i) + "%")
            
        battery_s = battery.battery_status() #instanciate the class in battery module
        status = battery_s.get_status() #take the actual status of the battery
        self.assertIn(status, battery_levels)

    def test_insert_drone(self):
        
        test_data = {}
        test_data["serial"] = "L0000"
        test_data["model"] = "testeo"
        test_data["weigth"] =  500
        test_data["battery"] = 100
        test_data["state"] = "ready"
        datajs = json.dumps(test_data, indent= 4)
        database = connect_db.db_connection()
        database.initial_state() #create the database if not exist for the full test
        self.assertTrue(database.insert_drone(datajs))

if __name__ == "__main__":
    unittest.main()