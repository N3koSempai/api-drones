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
                     state VARCHART(20) NOT NULL,
                     cargo VARCHAR(100))
                     """) #the table for drones
                
                curs.execute("CREATE TABLE MEDICATION (name VARCHART(30) NOT NULL,weigth INTEGER NOT NULL, code VARCHART(100) UNIQUE NOT NULL, image BLOB, loaded INTEGER)") 
                con.close() #close connection


    def insert(self,typedata , data):
        """insert drone to the database or insert medication.only change the value of typedata """
        con = sqlite3.connect("../db/drones.db") #connect to database
        curs = con.cursor() #set the cursor
        if typedata == 'insert_drone':
            try: #try to insert the data
                curs.execute("INSERT INTO DRONE VALUES(?,?,?,?,?,?)", (data['serial'],data['model'],data['weigth'],data['battery'],data['state'],'None')) #register a new drone
                con.commit()
                con.close()
                return True
            except: #handle error to insert data inside the database
                con.close()
                return False

        elif typedata == 'insert_medication':
            try:
                curs.execute("INSERT INTO MEDICATION VALUES(?,?,?,?,?)", (data['name'],data['weigth'],data['code'],data['img'],0))
                con.commit()
                con.close()
                return True
            except:
                return False
        elif typedata == 'loaded':
            curs.execute("UPDATE MEDICATION SET loaded = ? WHERE code = ?", (data['loaded'],data['code']) )
            con.commit()
            con.close()
        elif typedata == 'insert_cargo':
            try:
                print(data)
                curs.execute("UPDATE DRONE SET cargo = ? WHERE serial_number = ?", (data['code'],data['serial']) ) #search the drone for serial number and change the cargo 
                con.commit()
                con.close()
                return True
            except:
                con.close()
                return False
        elif typedata == 'test':
            try:
                curs.execute("INSERT INTO DRONE VALUES(?,?,?,?,?,?)", (data['serial'],data['model'],data['weigth'],data['battery'],data['state'],'None'))
                con.close()
                return True
            except:
                return False
        else:
            con.close()
            return False
        

    def get_data(self,typedata, data):
        
        con = sqlite3.connect("../db/drones.db") #connect to database
        curs = con.cursor() #set the cursor
        if typedata == 'get_drone':
            try:
                curs.execute("SELECT * FROM DRONE WHERE serial_number =(?)", (data['serial'],)) #get a specific drone stadistic
                data = curs.fetchone()
                con.close()
                return data
            except:
                con.close()
                return False
        elif typedata == 'get_medication':
            try:
                curs.execute("SELECT * FROM MEDICATION WHERE code =(?)", (data['code'],))#get a specific cargo medication
                data = curs.fetchone()
                con.close()
                return data
            except:
                con.close()
                return False
        elif typedata == 'get_available_drone':
            try:
                curs.execute("SELECT * FROM DRONE WHERE cargo = 'None'") # get drone without code in cargo, (available for loaded)
                data = curs.fetchall()
                con.close()
                return data
            except:
                con.close()
                return False
        elif typedata == "checking_loading":
            try:
                curs.execute("SELECT cargo FROM DRONE WHERE serial = (?)",  (data['serial'],)) # get cargo id from a specific drone
                data = curs.fetchall()
                if data != None:
                    self.get_data(typedata = "get_medication", data = data)
                con.close()
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