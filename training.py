#!/usr/bin/env python3
import mysql.connector
from mysql.connector import errorcode
import contextlib
import sys
class MySqlDatabase:
    def __init__(self,db,host,user,pwd):
        self.db = db
        self.host = host
        self.user = user
        self.pwd = pwd
        self.cnx = None

    @contextlib.contextmanager
    def connect(self):
        try:
            self.cnx = mysql.connector.connect(user=self.user,
                database=self.db,
                host=self.host,
                password=self.pwd)
            print("Connection opened")
            yield self.cnx
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password",file=sys.stderr)
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exists",file=sys.stderr)
        except Exception as e:
            print(str(e),file=sys.stderr)
        else: 
            self.cnx.close()
            print("Closed connection ..")
        return

s = MySqlDatabase("EMM","127.0.0.1","emm_op","em8")
#with s.connect() as cur:
    #print("Inside loop !")

def func_keywords(a="aaa",b="bbb",c="ccc"):
    print("a = {}, b = {}, c = {}".format(a,b,c))

json = {
        "a" : "nopeA",
        "b" : "nopeB"
        }
func_keywords(**json)
func_keywords(a="insidecall")

