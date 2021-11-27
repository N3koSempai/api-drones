import hug
import json

from hug.types import JSON
from modules import logics, connect_db
from hug import output_format

count = 0
dbc = connect_db.db_connection()
dbc.initial_state()
@hug.get()
@hug.http()
def get(typedata = hug.types.text, data = hug.types.JSON): #handle the get petition
    if typedata == 'get_drone' or typedata == 'get_medication' or typedata == 'get_available_drone': #handle petition for a single element
        res = dbc.get_data(typedata, data)
        return res
    
    elif typedata == 'test':
        return True

        
@hug.post(output_format = JSON)
@hug.http(typedata = hug.types.text, data = hug.types.JSON)
def post(typedata , data):
    global count
    if typedata == 'insert_drone' and count <= 10:
        count = count + 1
        res = dbc.insert(typedata,data)

        return res
    elif typedata == 'insert_medication':
        res = dbc.insert(typedata,data)
        return res

    elif typedata == 'test':
        return True
    return False