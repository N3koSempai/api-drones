from falcon import http_error, status_codes
import hug
import json
import falcon
import threading
from modules import connect_db
import asyncio
import os

#gobal variable
count = 0
fields = ['serial','model','weigth','battery','state','with cargo?']
accept_model = {'Lightweight': 100, 'Middleweight': 200, 'Cruiserweight': 300, 'Heavyweight' :500}
keys_model = accept_model.keys()
respond = {'result_of_your_query': 'Null'}

dbc = connect_db.db_connection()
dbc.initial_state()


os.chdir(os.path.dirname(os.path.realpath(__file__)))


class Drone(object):
    """
    Class for drone
    """



    @hug.post('/drone',output = hug.output_format.json, input = hug.input_format.json, )
    @hug.http(accept=('POST'))
    def drone(data: hug.types.json): #handle the petition
        res = dbc.get_data(typedata = 'get_drone', data = data) #search in database
        if res == None or res == False: #if dont have.
            raise falcon.HTTPError(falcon.HTTP_404) #raise a error not found
        res = dict(zip(fields,res)) #format with names of field before response
        return res

    @hug.post('/server_test',output = hug.output_format.json, input = hug.input_format.json )
    @hug.http(accept=('POST'))
    def server_test():
        return True

    @hug.post('/medication',output = hug.output_format.json, input = hug.input_format.json )
    @hug.http(accept=('POST'))
    def medication(data: hug.types.json):
        res = dbc.get_data(typedata = 'get_medication', data =data)
        if res == None or res == False:
            raise falcon.HTTPError(falcon.HTTP_404)
        return res

    @hug.get('/available_drone',output = hug.output_format.json)
    @hug.http(accept=('GET'))
    def available_drone(data: hug.types.json):
        res = dbc.get_data(typedata = 'get_available_drone', data = 0)
        if res == None or res == False:
            raise falcon.HTTPError(falcon.HTTP_404)
        return res

    @hug.post('/checking_loading',output = hug.output_format.json, input = hug.input_format.json) #cheking if the drone are loaded or not
    @hug.http(accept=('POST'))
    def cheking_loading(data: hug.types.json):
        res = dbc.get_data(typedata = 'get_drone', data =data)
        if res == None or res == False:
            raise falcon.HTTPError(falcon.HTTP_404)
        respond['result_of_your_query'] = 'True' #show the consulting is correct
        respond['is loading with'] = res[5] #get only the code of cargo
        return respond

    @hug.post('/checking_battery',output = hug.output_format.json, input = hug.input_format.json) #checking a battery level for a given drone
    @hug.http(accept=('POST'))
    def checking_battery(data: hug.types.json):
        res = dbc.get_data(typedata = 'get_drone', data =data)

        if res == None or res == False:
            raise falcon.HTTPError(falcon.HTTP_404)
        respond['result_of_your_query'] = (str(res[3]) + '%')
        return respond



    @hug.post('/insert_drone',output = hug.output_format.json, input = hug.input_format.json) #handle the post petition
    @hug.http(accept=('POST'))
    def insert_drone(data: hug.types.json):
        global temp #use the specific dict for errors result
        count = dbc.get_data(typedata = 'get_all_drone', data = data)
        count = len(count)
        if count + 1 > 10:
            raise falcon.HTTPError(falcon.HTTP_404, title='you have reached the maximun capacity for drones')
            
        if len(data['serial']) > 100 or data['model'] not in keys_model: #return false is over 100 char
            raise falcon.HTTPError(falcon.HTTP_404,title="the format of your data is incorrect")
        
        data['battery'] = 100
        data['state'] = 'IDLE'
        temp = data['model'] #get the model name for the input data
        size = accept_model[temp] #search in dict the weigth 
        data['weigth'] = size #set data weigth in the data for registering in db
        res = dbc.insert(typedata = 'insert_drone',data = data) #call to insert the data in db
        if res == None or res == False:
            raise falcon.HTTPError(falcon.HTTP_404, title = 'the serial is in used for other drone')
        respond['result_of_your_query'] = res
        return respond

    @hug.post('/insert_medication',output = hug.output_format.json, input = hug.input_format.json)
    @hug.http(accept=('POST'))
    def insert_medication(data: hug.types.json):
        for i in data['name']: #test format in name for medication item
            underscore_name = False
            letters_name = i.isalpha() #is a letter
            number_name = i.isdigit() #is a digit
            if i == '-' or i == '_':
                underscore_name = True
            if letters_name == True or number_name == True or underscore_name == True: #if is not invalid continue loops 
                continue
            else:
                raise falcon.HTTPError(falcon.HTTP_404, title = 'bad format in the name of medication') 
                

        for i in data['code']:#test format in code for medication item
            underscore_code = False
            number_code = i.isdigit() 
            uppercase = i.isupper()
            if i == '_':
                underscore_code = True
            if underscore_code == True or number_code == True or uppercase == True:
                continue
            else:
                raise falcon.HTTPError(falcon.HTTP_404, title = 'bad format in the code of medication') 

        res = dbc.insert(typedata = 'insert_medication',data = data) 
        respond['result_of_your_query'] = res
        return respond

    @hug.post('/insert_cargo', output = hug.output_format.json, input = hug.input_format.json)
    @hug.http(accept=('POST'))
    def insert_cargo(data: hug.types.json):
        res = dbc.get_data(typedata = "get_drone",data = data) #get if that drone have cargo 
        loaded = dbc.get_data(typedata = 'get_medication', data = data)# try if that cargo is already loaded
    
        if loaded == None or res == None: #search if the drone and medication item exist
            raise falcon.HTTPError(falcon.HTTP_404, title = "you dont have this drone or medication register") 

        elif loaded[4] == 1: #test if already loaded
            raise falcon.HTTPError(falcon.HTTP_404, title = "this package is has already loaded. create a new medication package with other code or chek this drone") 

        elif res[3] < loaded[1]: #
            raise falcon.HTTPError(falcon.HTTP_404, title = "the weigth of the cargo is higher than the capacity of the drone")
           
        elif res[5] == 'None' and loaded[4] == 0: #is if empty?

            res = dbc.insert(typedata = 'insert_cargo',data = data) #set the serial of new cargo
            change_loaded = {} #dict with medication code and the status changed to loaded
            change_loaded['loaded'] = 1
            change_loaded['code'] = loaded[2]
            dbc.insert(typedata='loaded',data = change_loaded)
            respond['result_of_your_query'] = res
            return respond
        else:
            raise falcon.HTTPError(falcon.HTTP_404)
