#!/usr/bin/env python3

import os.path
import json
import sys
import logging as log

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
    tables = dict()
    analysis = dict()
    databases = dict()
    sources = dict()

    mail = DEFAULT_MAIL = "nicolas.gailly@orange.ch"
    mail_server = DEFAULT_MAIL_SERVER = "localhost"
    sms_numbers = DEFAULT_SMS_NUMBERS = ["0787878027"]
    footer = DEFAULT_FOOTER = "Powered by Orange."
    
    @classmethod
    def parse_file(klass,file_name):
        """Parse the config file. """
        json_ = None
        try:
            with open(file_name,"r") as file:
                json_ = json.load(file)
        except IOError as e:
            log.error("Error while reading config file : {0}".format(e))
            raise e
        else:
            return Config.parse_json(json_)


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
        if "databases" in json:
            noerr = noerr and self.handle_databases(json["databases"])
            #log.debug("Databases dict : {}".format(self.databases))
        if "tables" in json:
            noerr = noerr and self.handle_tables(json["tables"])
            #log.debug("Tables dict : {}".format(self.tables))
        if "sources" in json:
            noerr = noerr and self.handle_sources(json["sources"])
            #log.debug("Sources dict : {}".format(self.sources))
        if "analysis" in json:
            noerr = noerr and self.handle_analysis(json["analysis"])
            #log.debug("Analysis dict : {}".format(self.analysis))
        if "alert" in json: self.handle_alert(json["alert"]) 
        if noerr == True:
            log.info("Config file parsed ... Ok :)")
        else:
            log.warning("Config file parsed ... Error  // ! \\\\")
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
                log.warning("Database info for table % is not known.Please specify before")
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
                    log.warning("Source {} specified in analysis {} does not correspond to anything.Skip.".format(source_name,a.name))
                    noerr = False
                    continue
                a.sources.append(self.sources[source_name])

            algos = []
            for algo in a.algorithms:
                if algo not in globals():
                    noerr = False
                    log.warning("Algorithm {} not recognized. Please lookup in algorithm/__init__.py to see if you import it well".format(algo))
                    continue
                ## instantiate the class
                algos.append(globals()[algo](a,a.options))
            a.algorithms = algos
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
                log.warning("Table {} not recognized in the source {} in configuration.".format(s.table,s.name))
                continue
            s.table = self.tables[s.table]
            self.sources[s.name] = s
        return noerr
    
    @classmethod
    def handle_alert(self,subjson):
        """Parse and store relevant information regarding the alerting event system"""
        self.mails = subjson["mails"] if "mails" in subjson else DEFAULT_MAIL
        self.mail_server = subjson["mail_server"] if "mail_server" in subjson else DEFAULT_MAIL_SERVER
        self.sms_numbers = subjson["sms_numbers"] if "sms_numbers" in subjson else DEFAULT_SMS_NUMBER
        self.footer = subjson["footer"] if "footer" in subjson else DEFAULT_FOOTER
        

import unittest

class ConfigTest(unittest.TestCase):

    def test_parse_nonexistent_file(self):
        file_name = "non_exist"
        self.assertRaises(FileNotFoundError,Config.parse_file,file_name)

    def test_parse_empty_json(self):
        json = dict()
        self.assertIsNone(Config.parse_json(json))

    def test_parse_good_json(self):
        data = {
                "databases" : [
                    { "host":"127.0.0.1",
                        "dbtype":"mysql",
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
                            { "name": "moving_average",
                                "sources": "mss_onnet",
                                "window":"10",
                                "slice":"5",
                                "period":1,
                                "nb_periods":3,
                                "algorithm":"Generic"
                                } ]
                            }
        self.assertTrue(Config.parse_json(data))
        for n,s in Config.databases.items():
            self.assertIsInstance(s,Database)
        for n,s in Config.tables.items():
            self.assertIsInstance(s,Table)

        for n,s in Config.sources.items():
            self.assertIsInstance(s,Source)
            self.assertIsInstance(s.table,Table)

        for n,s in Config.analysis.items():
            self.assertIsInstance(s,Analysis)


if __name__ == '__main__':
    unittest.main()
