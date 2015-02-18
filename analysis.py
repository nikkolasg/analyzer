import sys
import logging as log
import util
from report import Report
from parser import args
class Analysis:
    global arg
    """ This class is used to describe an analysis we want to make.
    It is generally composed of a name (or id ),a source name (for now, later we may 
    implement a multi source analysis), some fields to analyze,
    with some conditions (for now Sql where clause statements)
    and one or multiple  algorithm name, followed by options for theses algorithms"""

    def __init__(self,name,sources,algorithms,period,nb_periods,slice,window=1,opts = {}):
        self.name = name
        self.sources = sources
        self.algorithms = util.listize(algorithms)
        self.slice = slice
        self.period = period 
        self.nb_periods = nb_periods
        self.window = window
        ## options for the algorithm
        self.options = opts
        self.report = Report()
        self.report.store_message(Report.DEBUG,"Analysis {} with :".format(name))
        self.report.store_message(Report.DEBUG,"\t-{} sources".format(len(sources)))
        self.report.store_message(Report.DEBUG,"\t-{} algorithm".format(algorithms))
        self.report.store_message(Report.DEBUG,"\t-{} periods of {} secs".format(nb_periods,period))
        self.report.store_message(Report.DEBUG,"\t-slice of {} secs".format(slice))
        self.report.store_message(Report.DEBUG,"\t-window size of {}".format(window)) 

    def reports(self):
        """Will print the reports and graph according to args"""
        if args.graphs: 
            fname = util.now2str() + "_" + self.name + ".png"
            self.report.save_graph(fname)
        self.report.summary()
    
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

        if "algorithms" not in json:
            log.warning("No algorithms specified in analysis part of json")
            return None
        algorithms = json["algorithms"]
        del json["algorithms"]

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
        
        if slice > period:
            log.error("Analysis {} has a slice {} greater than its period {}. Invalid parameters.")
            main.cleanup(code = 1)

        return Analysis(name,sources,algorithms,period,nb_periods,slice,window,options)
        


