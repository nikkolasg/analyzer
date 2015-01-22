#!/usr/bin/env python3

import os.path
import json
import sys

## custom import
import database
import table
import source

from algorithm import *
class Config(object):
    """Class that handles the parsing of the config file 
    and that store the differents structures,i.e. store all sources
    objects defined, all analysis objects etc """
    file_name = file_name
    tables = dict
    analysis = dict
    database = dict
    sources = dict


    @classmethod
    def parse(klass,file_name):
        """Parse the config file. """
        json = None
        ## could do exception handling here, but is better at upper level (orchestrator)
        with open(file_name,"r") as file:
            json = json.load(file)

        interpret_json(json)

    @classmethod
    def interpret_json json
        """Will iterate through the json and will instanciate
        every objects it recognizes. will left out entries it does not know about"""
        for type,subjson in json.items():
            if type == "databases":
                Config.handle_databases(subjson)
            elif type == "tables":
                Config.handle_tables(subjson)
            elif type == "analysis":
                Config.handle_analysis(subjson)
            elif type == "sources":
                Config.handle_sources(subjson)
            else:
                print("Type {} not recongnized.Skip." % type,file=sys.stderr)

    @classmethod
    def handle_databases(subjson):
        for descr in subjson:
            d = Database.parse_json(descr)
            if d: databases[d.name] = d

    @classmethod
    def handle_tables(subjson):
        """ Parse and instantiate the table objects. It also link the database
        part of the table to the instance"""
        for descr in subjson:
            t = Table.parse_json(descr)
            if not t: next
            if t.database not in databases: 
                print("Database info for table % is not known.Please specify before")
                next
            t.database = databases[t.databases]
            tables[t.name] = t
             

    @classmethd
    def handle_analysis(subjson):
        """Parse and instantiate the analysis object. It also link the
        source part & algorithm part"""
        for descr in subjson:
            a = Analysis.parse_json(descr)
            if not a: next
            snames = a.sources
            a.sources = []
            for source_name in snames:
                if source_name not in sources:
                    print("Source {} specified in analysis {} does not correspond to anything.Skip.",% source_name,file=sys.stderr)
                    next
                a.sources.append(sources[source_name])

            if a.algorithm not in globals():
                print("Algorithm {} not recognized. Please lookup in algorithm/__init__.py to see if you import it well" % a.algorithm,file=sys.stderr)
                next
            ## instantiate the class
            a.algorithm = globals()[a.algorithm](a.options)

    def handle_sources(subjson):
        """ Parse and instanciate sources object with object references linked"""
        for descr in subjson:
            s = Source.parse_json(descr)
            if not s: next
            if s.table not in tables:
                print("Table {} not recognized in the source {} in configuration." % (s.table,s.name),file=sys.stderr)
                next
            sources[s.name] = s


                    





