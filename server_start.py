from falcon import http_error, status_codes
import hug
import json
import falcon
from requests.api import get
from requests.models import Response
from modules import connect_db

#gobal variable
count = 0

accept_model = {'Lightweight': 100, 'Middleweight': 200, 'Cruiserweight': 300, 'Heavyweight' :500}
keys_model = accept_model.keys()


dbc = connect_db.db_connection()
dbc.initial_state()

#@hug.get('/')
#@hug.http()
#def hello():
#    return "hello"

@hug.post('/drone',output = hug.output_format.json, input = hug.input_format.json)
@hug.http(accept=('GET'))
def drone(data: hug.types.json): #handle the get petition
    res = dbc.get_data(typedata = 'get_drone', data = data)
    if res == 'null':
        raise http_error(status_codes.HTTP_404)
        
    return res

@hug.post('/server_test',output = hug.output_format.json, input = hug.input_format.json )
@hug.http(accept=('GET'))
def server_test():
    return True

@hug.post('/medication',output = hug.output_format.json, input = hug.input_format.json )
@hug.http(accept=('GET'))
def medication(data: hug.types.json):
    res = dbc.get_data(typedata = 'get_medication', data =data)
    res = json.dumps(res)
    return res

@hug.post('/available_drone',output = hug.output_format.json, input = hug.input_format.json)
@hug.http(accept=('GET'))
def available_drone(data: hug.types.json):
    res = dbc.get_data(typedata = 'get_available_drone', data =data)
    res = json.dumps(res)
    return res

@hug.post('/cheking_loading',output = hug.output_format.json, input = hug.input_format.json) #cheking if the drone are loaded or not
@hug.http(accept=('GET'))
def cheking_loading(data: hug.types.json):
    res = dbc.get_data(typedata = 'checking_loading', data =data)
    res = json.dumps(res)
    return res

@hug.post('/checking_battery',output = hug.output_format.json, input = hug.input_format.json) #checking a battery level for a given drone
@hug.http(accept=('GET'))
def checking_battery(data: hug.types.json):
    res = dbc.get_data(typedata = 'checking_battery', data =data)
    res = json.dumps(res)
    return res



@hug.post('/insert_drone',output = hug.output_format.json, input = hug.input_format.json) #handle the post petition
@hug.http(accept=('POST'))
def insert_drone(data: hug.types.json):
    global count
    if len(data['serial']) > 100 or data['model'] not in keys_model: #return false is over 100 char
        error_format = "the format of your data is incorrect"
        return  json.dumps(error_format)
    data['battery'] = 100
    data['state'] = 'IDLE'
    temp = data['model'] #get the model name for the input data
    size = accept_model[temp] #search in dict the weigth 
    data['weigth'] = size #set data weigth in the data for registering in db
    res = dbc.insert(typedata = 'insert_drone',data = data) #call to insert the data in db
    count = count + 1
    res = json.dumps(data)
    return res

@hug.post('/insert_medication',output = hug.output_format.json, input = hug.input_format.json)
@hug.http(accept=('POST'))
def insert_medication(data: hug.types.json):
    for i in data['name']: #test format in name for medication item
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

    for i in data['code']:#test format in code for medication item
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

@hug.post('/insert_cargo', output = hug.output_format.json, input = hug.input_format.json)
@hug.http(accept=('POST'))
def insert_cargo(data: hug.types.json):
    res = dbc.get_data(typedata = "get_drone",data = data) #get if that drone have cargo 
    loaded = dbc.get_data(typedata = 'get_medication', data = data)# try if that cargo is already loaded
    
    if loaded == None or res == None: #search if the drone and medication item exist
        r = "you dont have this drone or medication register"
        return json.dumps(r)
    elif loaded[4] == 1: #test if loaded already
        r = "this package is has already loaded. create a new medication package with other code or chek this drone"
        return json.dumps(r)
    elif res[3] < loaded[1]: #
        r = "the weigth of the cargo is higher than the capacity of the drone"
        return json.dumps(r)
    elif res[5] == 'None' and loaded[4] == 0: #is if empty?
        print(res)
        res = dbc.insert(typedata = 'insert_cargo',data = data) #set the serial of new cargo
        change_loaded = {} #dict with medication code and the status changed to loaded
        change_loaded['loaded'] = 1
        change_loaded['code'] = loaded[2]
        dbc.insert(typedata='loaded',data = change_loaded)
        return json.dumps(res)
    else:
        return False
    
    

    