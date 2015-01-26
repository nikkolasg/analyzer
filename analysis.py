import sys
import logging as log
import util
from report import Report

class Analysis:
    global arg
    """ This class is used to describe an analysis we want to make.
    It is generally composed of a name (or id ),a source name (for now, later we may 
    implement a multi source analysis), some fields to analyze,
    with some conditions (for now Sql where clause statements)
    and an algorithm name, followed by options for this algorithm"""

    def __init__(self,name,sources,algorithm,period,nb_periods,slice,window=1,opts = {}):
        self.name = name
        self.sources = sources
        self.algorithm = algorithm
        self.slice = slice
        self.period = period 
        self.nb_periods = nb_periods
        self.window = window
        ## options for the algorithm
        self.options = opts
        self.report = Report()

    
    @classmethod
    def parse_json(self,json):
        """Read and set the corresponding members. Raise error if 
        found an aberration, or missing value"""
        if "name" not in json:
            log.warning("No name specified in analysis part of json")
            return None
        name = json["name"]
        if "sources" not in json: 
            log.warning("No source name specified in analysis part of  json")
            return None
        sources = util.listize(json["sources"])
        del json["sources"]

        if "algorithm" not in json:
            log.warning("No algorithm specified in analysis part of json")
            return None
        algorithm = json["algorithm"]
        del json["algorithm"]

        if "period" not in json:
            log.warning("No period size specified in analysis part of json")
            return None
        period = json["period"]
        del json["period"]

        if "nb_periods" not in json:
            log.warning("No nb_periods size specified in analysis part of json")
            return None
        nb_periods = json["nb_periods"]
        del json["nb_periods"]

        if "slice" not in json:
            log.warning("No slice size specified in analysis part of json")
            return None
        slice = json["slice"]
        del json["slice"]

        if "window" in json:
            window = json["window"]
            del json["window"]
        else:
            window = 1
        options = json.copy()

        return Analysis(name,sources,algorithm,period,nb_periods,slice,window,options)
        


