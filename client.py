import requests

if __name__== "__main__":
    url = "http://127.0.0.1:8000/insert_drone" # remember change the url before the petition
    
    insert_data_medic = {"data": {"name": "espirulina23_", "weigth": 20 , 'code': "A23FS", 'img': 12322354676878}} #medication insert arguments
    insert_cargo = {"data": {'code': "A23FS", "serial": "L30030"}} #for asignet a cargo to a drone. !IMPORTANT! the serial and the cargo has to exist
    databattery = {"data": {'serial': "L30030"}} #get the battery for a specific drone
    insert_drone = {'data': {'serial': 'L30030','model':'Middleweight'}}
    get_drone = {"data": {"serial": "L30030"}} #get drone information. !IMPORTANT! change the serial number for an existing one
    
    #discoment for use diferent request
    #for insert new drone
    url = "http://127.0.0.1:8000/insert_drone" # remember change the url before the petition
    response = requests.post(url, json = insert_drone) #change the argument json to any you want to try or try empty for a default response
    
    #for get any drone by unique serial_number
    # url = "http://127.0.0.1:8000/drone"  
    #response = request.post(url, json = get_drone)

    #for insert medication item before asignet
    #url = "http://127.0.0.1:8000/medication" 
    #response = request.post(url, json = insert_data_medic)
    
    #for check the battery
    #url = "http://127.0.0.1:8000/checking_battery" 
    #response = request.post(url, json = databattery)

    #see available drone
    #url = "http://127.0.0.1:8000/available_drone"
    #response = request.get(url)

    #cheking is load or not
    #url = "http://127.0.0.1:8000/checking_loading"
    #response = request.post(url, json = get_drone)

    #insert cargo
    #url = "http://127.0.0.1:8000/insert_cargo"
    #response = request.post(url, json = insert_cargo)
    
    
    
    
    print(response.content) #change for other option. example = response.headers
