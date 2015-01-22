#!/usr/bin/env python3
import unittest

class Fetcher:
    """This class is responsible for fetching the data out 
    of sources according to certain criterions (data)"""
    def __init__(self):
       self.cache = dict()

    def __str__(self):
        return "Fetcher : "



class FetcherTest(unittest.TestCase):
    """ Simple test to learn unit testing """
    def test_credentials(self):
       pass 


if __name__ == '__main__':
   unittest.main() 

