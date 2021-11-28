import hug
import json

from hug.types import json
from requests.api import get
from modules import logics, connect_db
from hug import output_format

#gobal variable
count = 0
accept_model = ['Lightweight', 'Middleweight', 'Cruiserweight', 'Heavyweight']


dbc = connect_db.db_connection()
dbc.initial_state()

#@hug.get('/')
#@hug.http()
#def hello():
#    return "hello"

@hug.get('/drone',output = hug.output_format.json)
@hug.http(accept=('GET'))
def drone(data: hug.types.json): #handle the get petition
    res = dbc.get_data(typedata = 'get_drone', data = data)
    res = json.dumps(res)
    return res

@hug.get('/server_test',outpout = hug.output_format.json)
@hug.http(accept=('GET'))
def server_test():
    return True

@hug.get('/medication',outpout = hug.output_format.json)
@hug.http(accept=('GET'))
def medication(data: hug.types.json):
    res = dbc.get_data(typedata = 'get_medication', data =data)
    res = json.dumps(res)
    return res

@hug.get('/available_drone',outpout = hug.output_format.json)
@hug.http(accept=('GET'))
def available_drone(data: hug.types.json):
    res = dbc.get_data(typedata = 'get_available_drone', data =data)
    res = json.dumps(res)
    return res

@hug.get('/cheking_loading',outpout = hug.output_format.json)
@hug.http(accept=('GET'))
def cheking_loading(data: hug.types.json):
    res = dbc.get_data(typedata = 'checking_loading', data =data)
    res = json.dumps(res)
    return res

@hug.get('/checking_battery',outpout = hug.output_format.json)
@hug.http(accept=('GET'))
def checking_battery(data: hug.types.json):
    res = dbc.get_data(typedata = 'checking_battery', data =data)
    res = json.dumps(res)
    return res


#post method
@hug.post('/insert_drone',output = hug.output_format.json) #handle the post petition
@hug.http(accept=('POST'))
def insert_drone(data: hug.types.json):
    global count
    if len(data['serial']) > 100 or data['model'] not in accept_model or data['weigth'] > 500: #return false is over 100 char
        return False 
    res = dbc.insert(data)
    count = count + 1
    res = json.dumbs(res)
    return res

@hug.post('/insert_medication',output = hug.output_format.json)
@hug.http(accept=('POST'))
def insert_medication(data: hug.types.json):
    for i in data['name']: #test format in name for medication.
        underscore_name = False
        letters_name = i.isalpha() #is a letter
        number_name = i.isdigit() #is a digit
        if i == '-' or i == '_':
            underscore = True
        if letters_name == True or number_name == True or underscore_name == True: #if is not invalid continue loops 
            continue
        else:
            res = json.dumbs('bad format in the name of medication')
            return res #is invalid format 

    for i in data['code']:
        underscore_code = False
        number_code = i.isdigit()
        uppercase = i.isupper()
        if i == '_':
            underscore_code = True
        if underscore_code == True or number_code == True or uppercase == True:
            continue
        else:
            res = json.dumbs('bad format in the code of medication')
            return res #is invalid format


    res = dbc.insert(typedata = 'insert_medication',data = data)
    return res

@hug.put('/insert_cargo', outpot = hug.output_format.json)
@hug.http(accept=('PUT'))
def insert_cargo(data: hug.types.json):
    res = dbc.get_data(typedata = "get_drone",data = data) #get if that drone have cargo 
    loaded = dbc.get_data(typedata = 'get_medication', data = data)# try if that cargo is already loaded
    
    if loaded == None or res == None:
        return "you dont have this drone or medication register"
    elif loaded[4] == 1:
        return "this package is has already loaded. create a new medication package with other code"
    elif res[5] == 'None' and loaded[4] == 0: #is if empty?
        print(res)
        res = dbc.insert(typedata = 'insert_cargo',data = data) #set the serial of new cargo
        change_loaded = {} #dict with medication code and the status changed to loaded
        change_loaded['loaded'] = 1
        change_loaded['code'] = loaded[2]
        dbc.insert(typedata='loaded',data = change_loaded)
        return res
    else:
        return False
    
    

    