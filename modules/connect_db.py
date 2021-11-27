import os
import sqlite3
import json

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# dataset for test
#test_data = {}
#test_data["serial"] = 'L0000'
#test_data["model"] = 'Lightweight'
#test_data["weigth"] =  500               
#test_data["battery"] = 100
#test_data["state"] = 'IDLE'
#datajs = json.dumps(test_data, indent= 4)

class db_connection():


    def initial_state(self):
        """create the database if not exist with all data required"""
        try:
            os.mkdir("../db") #test if not exist the folder, create it other ways handle the exception

        except FileExistsError:
            pass
        try:
            f = open("../db/drones.db", "r")  #test if the database exist
            f.close()
            
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


    def insert(self,typedata , data):
        
        con = sqlite3.connect("../db/drones.db") #connect to database
        curs = con.cursor() #set the cursor
        if typedata == 'insert_drone':
            try: #try to insert the data
                curs.execute("INSERT INTO DRONE VALUES(?,?,?,?,?)", (data['serial'],data['model'],data['weigth'],data['battery'],data['state']))
                con.commit()
                con.close()
                return True
            except: #handle error to insert data inside the database
                con.close()
                return False
        elif typedata == 'insert_medication':
            try:
                curs.execute("INSERT INTO MEDICATION VALUES(?,?,?,?)", (data['name'],data['weigth'],data['code'],data['img']))
                con.commit()
                con.close()
                return True
            except:
                return False
        elif typedata == 'test':
            try:
                curs.execute("INSERT INTO DRONE VALUES(?,?,?,?,?)", (data['serial'],data['model'],data['weigth'],data['battery'],data['state']))
                con.close()
                return True
            except:
                return False 
        
    def get_data(self, data):
        clear_data = json.loads(data) #convert the input json data to dict
        con = sqlite3.connect("../db/drones.db") #connect to database
        curs = con.cursor() #set the cursor
        try:
            print("in try")
            curs.execute("SELECT * FROM DRONE WHERE serial_number =(?)", (clear_data['serial'],))
            data = curs.fetchall()
            con.close()
            print(data)
            return True
        except:
            con.close()
            return False


    def delete(self, data):
        clear_data = json.loads(data) #convert the input json data to dict
        con = sqlite3.connect("../db/drones.db") #connect to database
        curs = con.cursor() #set the cursor
        try:
            curs.execute("DELETE FROM DRONE WHERE serial_number =(?)", (clear_data['serial'],))
            con.commit()
            con.close()
            return True
        except:
            con.close()
            return False



#inst = db_connection()
#inst.initial_state()
#inst.insert_drone(datajs)
#print(inst.get_data(datajs))
#print(inst.delete(datajs))   #only for test