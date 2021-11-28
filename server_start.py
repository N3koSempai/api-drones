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
    elif typedata == "checking_loading":
        res = dbc.get_data(typedata, data)
    elif typedata == 'checking_battery':
        try:
            res = dbc.get_data(typedata = 'get_drone', data = data)
            return res[3]
        except:
            return False
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

    elif typedata == 'insert_cargo':
        res = dbc.get_data(typedata = "get_drone",data = data) #get if that drone have cargo 
        loaded = dbc.get_data(typedata = 'get_medication', data = data)
        #add here a system for try if that cargo is already loaded
        print(loaded)
        if loaded == None or res == None:
            return "you dont have this drone or medication register"
        elif loaded[4] == 1:
            return "this package is has already loaded. create a new medication package with other code"
        elif res[5] == 'None' and loaded[4] == 0: #is if empty?
            print(res)
            res = dbc.insert(typedata,data) #set the serial of new cargo
            change_loaded = {}
            change_loaded['loaded'] = 1
            change_loaded['code'] = loaded[2]
            change = dbc.insert(typedata='loaded',data = change_loaded)
            return res
        else:
            return False

    elif typedata == 'test':
        return True
    return False