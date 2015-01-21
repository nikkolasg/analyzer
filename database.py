#!/usr/bin/env python3
class Database(object):
    """Class storing the informations about one database
    such as the name login and password"""

    def __init__(self,host,db,login,password):
        self.host = host
        self.db = db
        self.login = login
        self.password = password


    def __str__(self):
       return """Host : {}
                 Database : {}
                 Login : {}
                 Password : {} """.format(self.host,self.db,self.login,"*" * len(self.passsword))

    @staticmethod
    def create(db_type,host,db,login,password):
        """ Factory method to create a database holder which can be used
        to execute multiple queries"""
        if db_type == "mysql":
            return MysqlDatabase(host,db,login,password)
        else:
            sys.stderr.print("Unknown type of database." % db_type)


import mysql.connector as sql
class MysqlDatabase(Database):
    """implementation of Sql database"""


    def __init__(self,host,db,login,password):
        Database.__init__(self,db,login,password)
        self.cursor = None
        self.connection = None

    def __enter__(self):
        """ context manager to autmatically close the connection after use
        Can be use like with Database.create(config) as sql:
        or in a variable but dont forger to call __exit__ after"""
        try:
           self.connection = sql.connect(host=self.host,
                   database=self.database,
                   login=self.login,
                   password=self.password)
           self.cursor = self.connection.cursor()
           print("Connection to the Mysql database created !")
           return self.cursor
        except sql.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                sys.stderr.print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                sys.stderr.print("Database does not exists")
            else:
                print(err)
            raise 
    
    def __exit__(self,*args):
        """ Close the connection to the db"""
        if self.cursor is not None: self.cursor.close()
        if self.connection is not None: self.connection.close()
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
        badConfig = {
                'host': '127.0.0.1',
                'database':"wrong"
                }
        badCredentials = {
                'host': '127.0.0.1',
                'database':'wrong',
                'user':'me',
                'password':"you"
                }

        self.assertRaises(TypeError,Database.create,**badConfig)
        sql = Database.create(**badCredentials)
        with self.assertRaises(sql.Error):
            with bad_sql as cursor:
                cursor.execute("show tables")

        



if __name__ == '__main__':
    unittest.main()
