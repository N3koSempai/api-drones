from falcon import http_error, status_codes
from flask import Flask
import time
from flask_resful import Resource, Api
import json
import threading
from modules import connect_db
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


def background_task():
    time.sleep(120)
    print('this is the background task')

class Drone(Resource):
    """
    Class for drone
    """


    def get(self):
        threading.Thread(target=background_task)