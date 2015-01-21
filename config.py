#!/usr/bin/env python3

import os.path
import json
import sys

class Config(object):
    """Class that handles the parsing of the config file 
    and that store the differents structures,i.e. store all sources
    objects defined, all analysis objects etc """
    file_name = file_name
    sources = dict
    analysis = dict

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








