#!/usr/bin/env python3
import unittest
import datetime
import logging as log
import database
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


    def retrieve_data(source,analyse):
        """Actually make and query the SQL statement"""
        """For now, the model is timestamp, field1,field2..., counter.
        There is a certain value in counter for certains values in fields.
        For this iteration, we do it very simply. Compute one query per source,
        and one source contains one type of data, i.e. will retrieve only one 'counter'"""
        json = []
        table = source.table
        sql = "SELECT " + table.time_field ", " + table.counter +
            "FROM " + table.table_name + 
            "WHERE " + source.where_clause 
        upper_ts = args.timeref.timestamp()
        min_sec = analyse.nb_periods * analyse.periods
        lower_ts = (args.timeref - datetime.timedelta(seconds=min_sec)).timestamp()
        sql += " AND " + table.time_field + " < " + upper_ts +
               " AND " + table.time_field + " > " + lower_ts + 
               " ORDER BY " + table.time_field + " DESC"

        db = source.database
        with db.connect() as cursor:
            log.debug("Fetcher query analyse {} -> source {} :\n{}".format(analyse.name,source.name,sql)
            res = cursor.query(sql)

        for timest,counter in res:
            json.append((timest, counter))
       
       ## TODO Cache data
       return json

from config import Config
from constants import *
class FetcherTest(unittest.TestCase):
    """ Simple test to learn unit testing """
    def test_retrieve_data(self):
        Config.parse_file(DEFAULT_CONF_FILE)
        name,anal = Config.analysis.popitem()
        name,source = Config.source.popitem()
        json = retrieve_data(source,anal)


if __name__ == '__main__':
   unittest.main() 

