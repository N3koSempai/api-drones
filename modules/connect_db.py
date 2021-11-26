import os
import sqlite3
import json

os.chdir(os.path.dirname(os.path.realpath(__file__)))

class db_connection():

    def initial_state(self):
        """create the database if not exist with all data required"""
        try:
            os.mkdir("../db") #test if not exist the folder, create it other ways handle the exception

        except FileExistsError:
            pass
        try:
            open("../db/drones.db", "r")  #test if the database exist
            
        except FileNotFoundError: #database doest'not exist
                con = sqlite3.connect("../db/drones.db") #create the database
                print("creating structure for the simulation")
                curs = con.cursor() #set the cursor
                curs.execute("""CREATE TABLE DRONE (
                    serial_number VARCHART(100) UNIQUE NOT NULL,
                    model VARCHART(20) NOT NULL,
                    weight_limit INTEGER NOT NULL,
                     battery INTEGER NOT NULL,
                     state VARCHART(20) NOT NULL)""") #the table for drones
                
                curs.execute("CREATE TABLE MEDICATION (name VARCHART(30) NOT NULL,weigth INTEGER NOT NULL, code VARCHART(100) UNIQUE NOT NULL, image BLOB)") 
                con.close() #close connection

    def insert_drone(self, data):
        clear_data = json.loads(data) #convert the input json data to dict
        con = sqlite3.connect("../db/drones.db") #connect to database
        curs = con.cursor() #set the cursor
        try: #try to insert the data
            curs.execute("INSERT INTO DRONE VALUES(?,?,?,?,?)", (clear_data['serial'],clear_data['model'],clear_data['weigth'],clear_data['battery'],clear_data['state']))
            con.commit()
            con.close()
            return True
        except: #handle error to insert data inside the database
            con.close()
            return False


