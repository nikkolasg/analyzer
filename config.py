#!/usr/bin/env python3

import os.path
import json
import sys

## custom import
from database import Database
from analysis import Analysis
from table import Table
from source import Source
from algorithm import *

class Config(object):
    """Class that handles the parsing of the config file 
    and that store the differents structures,i.e. store all sources
    objects defined, all analysis objects etc """
    CONF_FILE = "config.json"
    tables = dict()
    analysis = dict()
    databases = dict()
    sources = dict()


    @classmethod
    def parse_file(klass,file_name):
        """Parse the config file. """
        json = None
        try:
            with open(file_name,"r") as file:
                json = json.load(file)
        except IOError as e:
            print("Error while reading config file : {0}".format(e),file=sys.stderr)
            raise e
        else:
            return Config.parse_json(json)


    @classmethod
    def parse_json(self,json):
        """ parse a json. either coming from a file or directly built"""
        if len(json) == 0: 
            print("Nothing in the json...")
            return 
        return self.interpret_json(json)

    @classmethod
    def interpret_json(self,json):
        """Will iterate through the json and will instanciate
        every objects it recognizes. 
        will left out entries it does not know about and return False is there has
        been an error. otherwise return True"""
        noerr = True 
        for type,subjson in json.items():
            if type == "databases":
                noerr = noerr and self.handle_databases(subjson)
            elif type == "tables":
                noerr = noerr and self.handle_tables(subjson)
            elif type == "analysis":
                noerr = noerr and self.handle_analysis(subjson)
            elif type == "sources":
                noerr = noerr and self.handle_sources(subjson)
            else:
                print("Type {} not recongnized.Skip.".format(type),file=sys.stderr)
        return noerr

    @classmethod
    def handle_databases(self,subjson):
        noerr = True
        for descr in subjson:
            d = Database.parse_json(descr)
            if d is not None: 
                self.databases[d.name] = d
            else:
                noerr = False
        return noerr
                

    @classmethod
    def handle_tables(self,subjson):
        """ Parse and instantiate the table objects. It also link the database
        part of the table to the instance"""
        noerr = True
        for descr in subjson:
            t = Table.parse_json(descr)
            if t is None: 
                noerr = False
                continue
            if t.database not in self.databases: 
                print("Database info for table % is not known.Please specify before")
                noerr = False
                continue
            t.database = self.databases[t.database]
            self.tables[t.name] = t

        return noerr
             

    @classmethod
    def handle_analysis(self,subjson):
        """Parse and instantiate the analysis object. It also link the
        source part & algorithm part"""
        noerr = True
        for descr in subjson:
            a = Analysis.parse_json(descr)
            if a is None:
                noerr = False
                continue
            snames = a.sources
            a.sources = []
            for source_name in snames:
                if source_name not in self.sources:
                    print("Source {} specified in analysis {} does not correspond to anything.Skip.".format(source_name,a.name),file=sys.stderr)
                    noerr = False
                    continue
                a.sources.append(self.sources[source_name])

            if a.algorithm not in globals():
                noerr = False
                print("Algorithm {} not recognized. Please lookup in algorithm/__init__.py to see if you import it well".format(a.algorithm),file=sys.stderr)
                continue
            ## instantiate the class
            a.algorithm = globals()[a.algorithm](a.options)
            self.analysis[a.name] = a
        return noerr

    @classmethod
    def handle_sources(self,subjson):
        """ Parse and instanciate sources object with object references linked"""
        noerr = True
        for descr in subjson:
            s = Source.parse_json(descr)
            if s is None: 
                noerr = False
                continue
            if s.table not in self.tables:
                noerr = False
                print("Table {} not recognized in the source {} in configuration.".format(s.table,s.name),file=sys.stderr)
                continue
            self.sources[s.name] = s
        return noerr


import unittest

class ConfigTest(unittest.TestCase):

    def test_parse_nonexistent_file(self):
        file_name = "non_exist"
        self.assertRaises(FileNotFoundError,Config.parse_file,file_name)

    def test_parse_empty_json(self):
        json = dict()
        self.assertIsNone(Config.parse_json(json))

    def test_parse_good_json(self):
        json = {
                "databases" : [
                    { "host":"127.0.0.1",
                      "database":"EMM",
                      "user":"emm_op",
                      "password":"888"} ],
                "tables" : [
                    { "name": "MSS",
                      "table_name": "MON_MSS_STATS",
                      "time_field": "timest",
                      "fields":["type"],
                      "database":"EMM"}
                    ],
                "sources": [
                    { "name": "mss_onnet",
                      "table": "MSS",
                      "where_clause": "source = 5 AND type = 8" } ],
                 "analysis" : [
                     { "name": "moving average",
                       "sources": "mss_onnet",
                       "window":"10",
                       "slice":"5",
                       "algorithm":"Generic"
                       } ]
              }
        self.assertTrue(Config.parse_json(json))



if __name__ == '__main__':
    unittest.main()
