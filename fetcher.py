#!/usr/bin/env python3
import unittest

class Fetcher:
    """This class is responsible for fetching the data out 
    of the database according to certain criterions """

    def __init__(self,db,login,password):
        self.db = db
        self.login = login
        self.password = password
        
    
    def __str__(self):
        return "Database : " + self.db + ", login : " + self.login + ", password : " + ("*" * len(self.password))



class FetcherTest(unittest.TestCase):
    """ Simple test to learn unit testing """
    def test_credentials(self):
        db = "emm"
        login = "emm_op"
        password = "em7"
        fetcher = Fetcher(db,login,password)
        self.assertTrue(db in str(fetcher))
        self.assertTrue(login in str(fetcher))
        self.assertFalse(password in str(fetcher))



if __name__ == '__main__':
   unittest.main() 

