# api-drones

## set the enviroment
1 -donwload all file with git clone or zip
2- move to the donwload directory
3- install all the necessary library with this command in your commandline
```batch
pip install -r requirements.txt
```

## run test
```batch
python -m unittest
```

## run server
# in the command line use
```batch
hug -f server_api.py
```

## send and receive data from the api server
### you have two options here

Use a advanced client for send POST with json data
in the test I use the browser extension Restman

**advice: dont send enty post petition with restman,the client have error.**
**advice2: I include a client for tests. all posible operation have include in that client**
1- only open the file [client](https://github.com/N3koSempai/api-drones/blob/main/client.py)
2- comment the two line ```url = ...``` and ```response = req...```

3- uncomment the petition you want to use and run with python that file


>note: all endpoint use post and only one use get because is >not correctly send data in the body of a get petition.

## possible operations,arguments and help page

### the funtionality of this softwware
The cargo loaded in the drone is a code reference to the code of the medication package. 

### 1 - help/documentation page
make a GET request for ```http://127.0.0.1:8000```

### 2 - Insert a new drone
url = ```http://127.0.0.1:8000/insert_drone```

HTTP method: POST

key field: ```data```  without quotation marks

values field example: 
```json
{'code': "A23FS", "serial": "L30030"} 
```

### 3 - get a drone information
url = ```http://127.0.0.1:8000/drone```

HTTP method: POST

key field: ```data```  without quotation marks

values field example: 
```json
{"serial": "L30030"} 
```

### 4 - insert medication item before asignet
 url = ```http://127.0.0.1:8000/insert_medication```

HTTP method: POST

key field: ```data```  without quotation marks

values field example: 
```json
{"name": "espirulina23_", "weigth": 20 , 'code': "A25FS", 'img': 12322354676878}
```

**advice: the field img for image is a blob field you need to convert your image to binary before send**

>note: the standart solution for this requirement is save the img in a >folder an save in the db a reference to the position

### 5 - insert cargo after medication is register for reference
url = ```"http://127.0.0.1:8000/insert_cargo"```

HTTP method: POST

key field: ```data```  without quotation marks

values field example: 
```json
{'code': "A23FS", "serial": "L30030"}
```


### 6 - check battery
url = ```http://127.0.0.1:8000/checking_battery```

HTTP method: POST

key field: ```data```  without quotation marks

values field example: 
```json
{'serial': "L30030"}
```

### 6 - check is load or not
url = ```http://127.0.0.1:8000/checking_loading```

HTTP method: POST

key field: ```data```  without quotation marks

values field example: 
```json
{'serial': "L30030"}
```

### 7 - check available drone

url = ```http://127.0.0.1:8000/available_drone```

HTTP method: GET

without data in the body of the request