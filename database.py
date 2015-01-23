#!/usr/bin/env python3
import sys

class Database(object):
    """Class storing the informations about one database
    such as the name login and password.Database will be the name used to refer
    to this database"""

    def __init__(self,host,database,user,password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.name = database

    def __str__(self):
        return """Host : {}
                 Database : {}
                 Login : {}
                 Password : {} """.format(self.host,self.db,self.user,"*" * len(self.passsword))

    @classmethod
    def parse_json(klass,json):
        """Check existence of required field and send them to create"""
        h = dict()
        if "host" not in json:
            print("Host is not specified in database part",file=sys.stderr)
            return None
        h["host"] = json["host"]
        if "database" not in json:
            print("Database name is not specified in database part",file=sys.stderr)
            return None
        h["database"] = json["database"]
        if "user" not in json:
            print("User name is not specified in database part",file =sys.stderr)
            return None
        h["user"] = json["user"]
        if "password" not in json:
            print("Password is not specified in database part",file=sys.stderr)
            return None
        h["password"] = json["password"]
        if "dbtype" not in json:
            print("Type of database not specified in database part",file=sys.stderr)
            return None
        h["dbtype"] = json["dbtype"]
        return Database.create(**h)
        

    @classmethod
    def create(self,host="",database="",user="",password="",dbtype="mysql"):
        """ Factory method to create a database holder which can be used
        to execute multiple queries"""
        if dbtype == "mysql":
            return MysqlDatabase(host,database,user,password)
        else:
            print("Unknown type of database {0}.".format(dbtype),file=sys.stderr)
            return None


import mysql.connector 
from mysql.connector import errorcode

class MysqlDatabase(Database):
    """implementation of Sql database"""

    def __init__(self,host,database,user,password):
        Database.__init__(self,host,database,user,password)
        self.cursor = None
        self.connection = None

    def __enter__(self):
        """ context manager to autmatically close the connection after use
        Can be use like with Database.create(config) as sql:
        or in a variable but dont forger to call __exit__ after"""
        try:
           self.connection = mysql.connector.connect(host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password)
           self.cursor = self.connection.cursor()
           print("Connection to the Mysql database created !")
           return self.cursor
        except mysql.connector.Error as err:
           if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
               print("Something is wrong with your user name or password",file=sys.stderr)
           elif err.errno == errorcode.ER_BAD_DB_ERROR:
               print("Database does not exists",file=sys.stderr)
           else :
               print(err,file=sys.stderr)
           self.__exit__()

    def __exit__(self,*args):
        """ Close the connection to the db"""
        if self.cursor: self.cursor.close()
        if self.connection: self.connection.close()
        self.cursor = None
        self.connection = None
        print("Connection to the Mysql database closed ...")


import unittest
class DatabaseTestUnit(unittest.TestCase):
    def test_mysql_connection(self):
        """Simple test to check connection is going well or not"""
        config = {
                'host': '127.0.0.1',
                'database': "nicotest",
                'user': "ngailly",
                'password': "simonette2014"
                }




        def test_connection_bad_config(self):
            """Test connecting to mysql with bad config"""
        badConfig = {
                'host': '127.0.0.1',
                'database':"wrong"
                }
        sql = Database.create(**badConfig)
        #self.assertRaises(mysql.connector.errors.ProgrammingError,sql.__enter__)
        sql.__enter__()
        sql.__exit__()

    def test_connection_bad_credentials(self):
        """Test connecting to mysql with bad credentials"""
        badCredentials = {
                'host': '127.0.0.1',
                'database':'wrong',
                'user':'me',
                'password':"you"
                }
        sql = Database.create(**badCredentials)
        #self.assertRaises(mysql.connector.errors.ProgrammingError,sql.__enter__)
        sql.__enter__()
        sql.__exit__()


if __name__ == '__main__':
    unittest.main()
