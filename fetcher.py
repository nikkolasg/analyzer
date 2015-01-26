#!/usr/bin/env python3
import unittest
import datetime
import logging as log
import database
from parser import args
class Fetcher:
    """This class is responsible for fetching the data out 
    of sources according to certain criterions (data).
    The data going out of fetcher is in JSON format, such as
    time: TIMESTAMP,
    values: [v1]"""
    def __init__(self):
       self.cache = dict()
    
    def get_data(analyse):
        """ Main method. Pass it an analyze object, to retrieve data from.
        You can specify options here like window and width"""
        ## TODO : merge at the most possible the differents source fields required,
        ## to query as little as we can on the db
        json = {}
        for source in analyse.sources:
            json[source.name] = retrieve_data(analyse,source)
        return json

    def __str__(self):
        return "Fetcher : "


    def retrieve_data(self,source,analyse):
        """Actually make and query the SQL statement"""
        """For now, the model is timestamp, field1,field2..., counter.
        There is a certain value in counter for certains values in fields.
        For this iteration, we do it very simply. Compute one query per source,
        and one source contains one type of data, i.e. will retrieve only one 'counter'"""
        json = []
        sql = self.compute_sql(source,analyse)
        db = source.table.database
        return self.execute_sql(db,sql)
       
    def compute_sql(self,source,analyse):
        """Create the sql statement that is to be used in the analysis"""
        table = source.table
        sql =  "SELECT " + table.time_field + ", " + table.counter 
        sql += " FROM " + table.table_name  
        sql += " WHERE " + source.where_clause 
        upper_ts = int(args.timeref.timestamp())
        min_sec = analyse.nb_periods * analyse.period
        lower_ts = int((args.timeref - datetime.timedelta(seconds=min_sec)).timestamp())
        sql += " AND " + table.time_field + " BETWEEN "
        sql +=  str(lower_ts) + " AND " + str(upper_ts)
        sql += " ORDER BY " + table.time_field + " DESC"
        return sql

    def execute_sql(self,db,sql):
        json = []
        with db.connect() as cursor:
            log.debug("Fetcher query : \n{}".format(sql))
            cursor.execute(sql)
            for timest,counter in cursor:
                json.append((timest, counter))
        return json
       
from config import Config
from constants import *
import util
import main
class FetcherTest(unittest.TestCase):
    """ Simple test to learn unit testing """
    def test_retrieve_data(self):
        main.setup()
        Config.parse_file(DEFAULT_CONF_FILE)
        name,anal = Config.analysis.popitem()
        name,source = Config.sources.popitem()
        fetcher = Fetcher()
        json = fetcher.retrieve_data(source,anal)
        util.pprint_data(json)
        self.assertTrue(len(json) > 1)
        self.assertIsInstance(json.pop(),tuple)
        

if __name__ == '__main__':
   unittest.main() 

