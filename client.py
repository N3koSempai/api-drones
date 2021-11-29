import requests

if __name__== "__main__":
    url = "http://127.0.0.1:8000/drone" # remember change the url before the petition
    
    insert_data_medic = {"data": {"name": "espirulina23_", "weigth": 20 , 'code': "A25FS", 'img': 12322354676878}} #medication insert arguments
    insert_cargo = {"data": {'code': "A23FS", "serial": "L30030"}} #for asignet a cargo to a drone. !IMPORTANT! the serial and the cargo has to exist
    databattery = {"data": {'serial': "L30030"}} #get the battery for a specific drone
    insert_drone = {"data": {"serial": "L30055","model":"Middleweight"}}
    get_drone = {"data": {"serial": "L30055"}} #get drone information. !IMPORTANT! change the serial number for an existing one
    response = requests.post(url, insert_drone) #change the argument json to any you want to try or try empty for a default response
    print(response.content) #change for other option. example = response.headers
