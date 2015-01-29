#!/usr/bin/env python3

from fetcher import Fetcher
import logging as log
import formatter as f
from config import Config

def run_all():
    for name,analysis in Config.analysis.items():
        run_analysis(analysis)
    
def run_analysis(analysis):
    """Run a complete analysis from beginning to the end"""
    data = get_data_analysis(analysis)
    pdata = format_data(data,analysis)
    run_algorithm(analysis.algorithm,pdata)
    analysis.reports() 
    
def get_data_analysis(analysis):
    """Retrieve the data for a source"""
    fetcher = Fetcher()
    data = fetcher.get_data(analysis)
    log.debug("Fetcher got {} items ...".format(len(next(iter(data.values())))))
    return data

def get_data_parameters(parameters):
    """Retrieve the data from a list of parameters"""
    ## TODO

def format_data(data,analysis):
    """Transform the data so the algorithm will get what they want """
    pdata = f.format(data,analysis)
    log.debug("Format returned {} items...".format(len(next(iter(pdata.values())))))
    return pdata

def run_algorithm(algorithm,data):
    """Run an algorithm with the specified data"""
    algorithm.run(data)
