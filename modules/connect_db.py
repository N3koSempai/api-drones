import os
import sqlite3
import errno
from sqlite3.dbapi2 import Cursor
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
                    serial_number VARCHART(100) NOT NULL,
                    model VARCHART(20) NOT NULL,
                    weight_limit INTEGER NOT NULL,
                     battery INTEGER NOT NULL,
                     state VARCHART(20) NOT NULL)""") #the table for drones
                
                curs.execute("CREATE TABLE MEDICATION (name VARCHART(30) NOT NULL,weigth INTEGER NOT NULL, code VARCHART(100) NOT NULL, image BLOB NOT NULL)") 
                con.close() #close connection
            


    

inst = db_connection()
inst.initial_state()
        

