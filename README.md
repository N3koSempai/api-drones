# api-drones

## set the enviroment
1 -donwload all file with git clone or zip <br/>
2- move to the donwload directory <br/>
3- install all the necessary library with this command in your commandline <br/>
```batch
pip install -r requirements.txt
```

## run test
```batch
python -m unittest
```

## run server
 in the command line use:
```batch
hug -f server_api.py
```

## send and receive data from the api server
### you have two options here

1 -Use a advanced client for send POST with json data
in the test I use the browser extension Restman

**advice: dont send enty post petition with restman,the client have error.** <br/>
**advice2: I include a client for tests. all posible operation have include in that client** <br/>
1 - only open the file [client](https://github.com/N3koSempai/api-drones/blob/main/client.py) <br/>
2 - comment the two line ```url = ...``` and ```response = req...``` <br/>
3- uncomment the petition you want to use and run with python that file <br/>


>note: all endpoint use post and only one use get because is >not correctly send data in the body of a get petition.

## possible operations,arguments and help page

### the funtionality of this softwware
>(important thing you need know)

1- The cargo loaded in the drone is a code reference to the code of the medication package. <br/>
2- the models in the request need to by exactly one of this and the system asignet automatic weigth. <br/>
#### problem i had in the development of this api

**due to my little experience with api framework I selected a good library in python for that but this library have very low documentation and is not very**
**compatible with concurrency and parallelism functions.**
**so then it became impossible for me to implement multithrading or multiprocessing for background tasks.**
**this would be easy to solve with flask api framework but no time for refactor all the code.**
**the logical I would implement after that would not be complex.**
 example: <br/>
1 - a async function get drones state every 2 min and if it is not in IDLE state change to the next state (the drone and medication package is mark loaded when use the isert_cargo function correctly) <br/>
2 - insert a data with time , serial, cargo code and battery level to logs Table every 2 min <br/>
3 -  remove a 15% of battery at each change of state <br/>
4 - if drone return to IDLE remove the code in cargo field,and wait 2 minutes to go to 100% the battery <br/>



```json
{"Lightweight": 100, "Middleweight": 200, "Cruiserweight": 300, "Heavyweight" :500}
```

### 1 - help/documentation page
make a GET request for ```http://127.0.0.1:8000```

### 2 - Insert a new drone
url = ```http://127.0.0.1:8000/insert_drone``` <br/>
HTTP method: POST <br/>
key field: ```data```  without quotation marks <br/>

values field example: 
```json
{"serial": "L30030","model":"Middleweight"}
```

### 3 - get a drone information
url = ```http://127.0.0.1:8000/drone``` <br/>
HTTP method: POST <br/>
key field: ```data```  without quotation marks <br/>

values field example: 
```json
{"serial": "L30030"} 
```

### 4 - insert medication item before asignet
url = ```http://127.0.0.1:8000/insert_medication``` <br/>
HTTP method: POST <br/>
key field: ```data```  without quotation marks <br/>

values field example: 
```json
{"name": "espirulina23_", "weigth": 20 , "code": "A25FS", "img": 12322354676878}
```

### 5 - get a medication package information
url = ```http://127.0.0.1:8000/medication``` <br/>
HTTP method: POST <br/>
key field: ```data```  without quotation marks <br/>
values field example: 
```json
{ "code": "A25FS"}
```

**advice: the field img for image is a blob field you need to convert your image to binary before send**

>note: the standart solution for this requirement is save the img in a folder an save in the db a reference to the position

### 6 - insert cargo after medication is register for reference
url = ```"http://127.0.0.1:8000/insert_cargo"``` <br/>
HTTP method: POST <br/>
key field: ```data```  without quotation marks <br/>

values field example: 
```json
{"code": "A23FS", "serial": "L30030"}
```


### 7 - check battery
url = ```http://127.0.0.1:8000/checking_battery``` <br/>
HTTP method: POST <br/>
key field: ```data```  without quotation marks <br/>

values field example: 
```json
{"serial": "L30030"}
```

### 8 - check is load or not
url = ```http://127.0.0.1:8000/checking_loading``` <br/>
HTTP method: POST <br/>
key field: ```data```  without quotation marks <br/>

values field example: 
```json
{"serial": "L30030"}
```

### 9 - check available drone

url = ```http://127.0.0.1:8000/available_drone``` <br/>
HTTP method: GET <br/>
without data in the body of the request <br/>