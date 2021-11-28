import hug
import json

from hug.types import JSON
from modules import logics, connect_db
from hug import output_format

#gobal variable
count = 0
accept_model = ['Lightweight', 'Middleweight', 'Cruiserweight', 'Heavyweight']


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
            return res[3] #return only the battery field
        except:
            return False #exception or drone doest'not exist
    elif typedata == 'test':
        return True

    

@hug.post(output_format = JSON) #handle the post petition
@hug.http(typedata = hug.types.text, data = hug.types.JSON)
def post(typedata , data):
    global count

    if typedata == 'insert_drone' and count <= 10:
        
        if len(data['serial']) > 100 or data['model'] not in accept_model or data['weigth'] > 500: #return false is over 100 char
            return False 
        res = dbc.insert(typedata,data)
        count = count + 1
        return res
    elif typedata == 'insert_medication':
        for i in data['name']: #test format in name for medication.
            underscore_name = False
            letters_name = i.isalpha() #is a letter
            number_name = i.isdigit() #is a digit
            if i == '-' or i == '_':
                underscore = True
            if letters_name == True or number_name == True or underscore_name == True: #if is not invalid continue loops 
                continue
            else:
                return 'bad format in the name of medication' #is invalid format 

        for i in data['code']:
            underscore_code = False
            number_code = i.isdigit()
            uppercase = i.isupper()
            if i == '_':
                underscore_code = True
            if underscore_code == True or number_code == True or uppercase == True:
                continue
            else:
                return 'bad format in the code of medication'


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