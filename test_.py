from falcon import status_codes
from modules import  connect_db
import json
import unittest , os
import requests, asyncio
import server_start



class TestClass(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        self.data = {"data": {"serial": "L0000", "model": "chopter",'weigth':0,'battery': 100,'state': 'IDLE'}}
        self.datadict = {"serial": "L0001", "model": "chopter",'weigth':0,'battery': 100,'state': 'IDLE'}
        self.typedb = 'test' #tell a method is a test
        self.typedata = {"typedata": "test"}
        self.database = connect_db.db_connection()
        super(TestClass, self).__init__(*args, **kwargs)

    def test_db(self): # for this test delete the db because duplication error with a Unique field inside the db

        self.database.initial_state() #create the database if not exist for the full test
        self.assertTrue(self.database.insert(self.typedb, self.datadict))
    
    

    async def test_get_api_server_http(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        task1 = os.system("hug -f server_start.py")
        url = "http://127.0.0.1:8000/server_test"
        await task1
        asyncio.sleep(10)
        self.assertTrue(requests.post(url))



if __name__ == "__main__":
    unittest.main()