#!/usr/bin/env python3
##This module format a JSON according to come criterion in a analysis.
##Specifically, it will slice the original data, take #window points for each periods
import logging as log
import pdb
def format(json, analysis):
    newjson = {}
    for source_name,data in json.items():
        newjson[source_name] = format_data(data,
                                            analysis.slice,
                                            analysis.period,
                                            analysis.nb_periods,
                                            analysis.window) 

    return newjson

def format_data(data,slice,period,nb_periods,window):
    """Responsible for doing the slicing / windowing / perioding operations
    on a JSON formatted data, for one source. Format is [ (time,value),(time2,value2) ...]"""
    newjson = []
    if len(data) < 1: 
        log.debug("No data to format ...")
        return newjson
    i = 0 ## we suppose the first entry is the most recent one
    tslice = get_lower_bound(data[i][0],slice) 
    vslice = 0 ## value summing all values in a slice
    current_period = 0 ## how many periods have we done yet
    nb_points = 0 ## how many points have we taken by periodsd
    good_index = 0 ## the last point that falls exactly on our period. Use it to get the next good_index, like good_index - analysis.period
    #pdb.set_trace()
    while(i < len(data)):
        ## if wa have crossed a slice boundary, insert the value
        ## of the slice we computed into the new json
        if data[i][0] <= tslice:
            ## tslice+slice so that the value correspond to the more recent time
            ## either that or the oldest with just tslice, 
            ## depends on how u wanna see it
            newjson.append((tslice+slice,vslice))
            tslice = get_lower_bound(data[i][0],slice)
            vslice = 0
            nb_points += 1

        ## if we have sliced enough point for a week or a month(for a period),
        ## we gonna search to the precedent starting period directly
        if nb_points == window:
            nb_points = 0
            current_period += 1
            ## we have analyzed enough data, stop !
            if current_period == nb_periods: break
            ## this is the next timestamp that begins a new period
            next_ts = data[good_index][0] - period
            ## we take the upper bound of the precedent period
            ## that way any point before the exact precedent period starting point
            ## that may fall down under the SAME slice, will be evaluated
            next_bound = get_upper_bound(next_ts,slice)
            ## iterate as long as we dont find a good point,i.e. first time of slice
            while(data[i][0] > next_bound and i < len(data)): i += 1
            if i == len(data): break
            
            #found the first time of slice iterate until start of next period
            while(data[i][0] > next_ts and i < len(data)): 
                ## store the preceding values falling down under the same slice
                vslice += data[i][1]
                i += 1
            good_index = i
            tslice = get_lower_bound(data[i][0],slice) ## same for the slice 

        vslice += data[i][1]
        i += 1
    return newjson


def get_lower_bound(timest,slice):
    """Return the lower bound of time formatted by the slice var from the Epoch.
    i.e. if slice = 3600, timest = 3h15 ==> timest = 3h00
    if timest = 3h00, ==> return 2h00
    if timest = 3h15 ==> return 3h00"""
    return timest - slice if timest % slice == 0 else (timest - (timest % slice))

def get_upper_bound(timest,slice):
    """Same as lower_bound except return the upper bound ...;) 
    if 3h00 ==> return 3h00,
    if 3h15 ==> return 4h00"""
    return timest if timest % slice == 0 else (timest + (slice - (timest % slice)))



import unittest
from constants import *
from config import Config
import time
import json
import util
class FormatterTest(unittest.TestCase):

    def test_format_data_empty_json(self):
        """Test formatting with an empty json"""
        Config.parse_file(DEFAULT_CONF_FILE)
        json = {}
        self.assertEqual(0,len(format_data(json,0,0,0,0)))
    def test_format_data_normal(self):
        """Test formatting with a fully filled json structure"""
        slice = 10*60
        window = 2
        period = 3600
        nb_period = 2
        data = FormatterTest.construct_data()
        nbpoints = len(data)
        util.pprint_data(data)
        newdata = format_data(data,slice,period,nb_period,window)
        util.pprint_data(newdata)
        self.assertEqual(window*nb_period,len(newdata))

    @classmethod
    def construct_data(self,interval=5*60,total_time=3*3600):
        """ Construct a sample json with a simple y=2x linear curve
        spaced every 5mn and for 3h"""
        count = 0
        ts = int(time.time())
        ts = get_lower_bound(ts,interval)
        maxts = ts + total_time
        data = []
        while ts < maxts:
            data.append((ts,count))
            count += 2
            ts += interval
        return list(reversed(data))



if __name__ == '__main__':
    unittest.main()
