import requests

if __name__== "__main__":
    url = "http://127.0.0.1:8000/post"
    data = {"data": {"serial": "L30028", "model": "scorch",'weigth':100,'battery': 100,'state': 'IDLE'}}
    datam = {"data": {"name": "espirulina", "weigth": 20 , 'code': "A23FS", 'img': 12322354676878}}
    typedata = {"typedata": "insert_drone"} #change to inser_medication
    response = requests.post(url, params=typedata ,json = data)
    print(response.json())
