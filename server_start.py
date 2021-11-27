import hug
import json

from hug.types import JSON
from modules import logics, connect_db
from hug import output_format

dbc = connect_db.db_connection()
dbc.initial_state()




@hug.post(output_format = JSON)
@hug.http(typedata = hug.types.text, data = hug.types.JSON)
def post(typedata , data):
    if typedata == 'insert_drone' or typedata == 'insert_medication':
        res = dbc.insert_drone(typedata,data)
        #data = json.dumps(data)
        return res
    return False