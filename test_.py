from falcon import status_codes
from modules import battery, connect_db
import json
import unittest , os
import requests, asyncio
import server_start



class TestClass(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        self.data = {"data": {"serial": "L0000", "model": "chopter",'weigth':0,'battery': 100,'state': 'IDLE'}}
        self.datadict = {"serial": "L0000", "model": "chopter",'weigth':0,'battery': 100,'state': 'IDLE'}
        self.typedb = 'test' #tell a method is a test
        self.typedata = {"typedata": "test"}
        self.database = connect_db.db_connection()
        super(TestClass, self).__init__(*args, **kwargs)
        
    def test_battery_level(self):
        battery_levels = []
        for i in range(0, 101):
            battery_levels.append(str(i) + "%")
            
        battery_s = battery.battery_status() #instanciate the class in battery module
        status = battery_s.get_status() #take the actual status of the battery
        self.assertIn(status, battery_levels)

    def test_db(self): # for this test delete the db because duplication error with a Unique field inside the db

        self.database.initial_state() #create the database if not exist for the full test
        self.assertTrue(self.database.insert(self.typedb, self.datadict))
    
    

    async def test_get_api_server_http(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        task1 = os.system("hug -f server_start.py")
        url = "http://127.0.0.1:8000/post"
        await task1
        asyncio.sleep(1)
        await self.assertTrue(requests.post(url))



if __name__ == "__main__":
    unittest.main()