#!/usr/bin/env python3

from fetcher import Fetcher
import logging as log
import formatter as f
from config import Config
from parser import args
import copy
import functools
def run_all():
    if args.analysis :
        if args.analysis not in Config.analysis:
            log.error("Analysis specified in command line not known ... Abort.")
            exit(1)
        run_analysis(Config.analysis[args.analysis])
    else:
        for name,analysis in Config.analysis.items():
            run_analysis(analysis)
    
def run_analysis(analysis):
    """Run a complete analysis from beginning to the end"""
    data = get_data_analysis(analysis)
    pdata = format_data(data,analysis)
    for algo in analysis.algorithms:
        run_algorithm(algo,copy.deepcopy(pdata))
    analysis.reports() 
    
def get_data_analysis(analysis):
    """Retrieve the data for a source"""
    fetcher = Fetcher()
    data = fetcher.get_data(analysis)
    length = functools.reduce(lambda x,y: x+len(y),data.values(),0)
    log.debug("Fetcher got {} items ...".format(length))
    return data

def get_data_parameters(parameters):
    """Retrieve the data from a list of parameters"""
    ## TODO

def format_data(data,analysis):
    """Transform the data so the algorithm will get what they want """
    pdata = f.format(data,analysis)
    length = functools.reduce(lambda x,y: x+len(y),pdata.values(),0)
    log.debug("Format returned {} items...".format(length))
    return pdata

def run_algorithm(algorithm,data):
    """Run an algorithm with the specified data"""
    algorithm.run(data)
