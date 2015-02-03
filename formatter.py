#!/usr/bin/env python3
##This module format a JSON according to come criterion in a analysis.
##Specifically, it will slice the original data, take #window points for each periods
import logging as log
import pdb
import util
def format(json, analysis):
    newjson = {}
    #util.pretty(json,text = "JSON BEFORE FORMAT ")
    for source_name,data in json.items():
        newjson[source_name] = format_data(data,
                                            analysis.slice,
                                            analysis.period,
                                            analysis.nb_periods,
                                            analysis.window) 

    util.pretty(newjson,"JSON AFTER FORMAT ")
    return newjson

def format_data(data,slice,period,nb_periods,window):
    """Responsible for doing the slicing / windowing / perioding operations
    on a JSON formatted data, for one source. Format is [ (time,value),(time2,value2) ...]. The values must be ordered from the most recent to the oldest entries"""
    newjson = []
    if len(data) < 1: 
        log.debug("No data to format ...")
        return newjson
    i = 0 ## we suppose the first entry is the most recent one
    tslice = get_lower_bound(data[i][0],slice) ## the oldest time in current slice
    vslice = 0 ## value of the current slice 
    last_period_index = 0 ## index of the begining of the current period
    nb_points = 0 ## nb points we have for the current period. must not go higher
                  ## than the window parameters. The first point is always taken
    period_count = 0
    #pdb.set_trace()
    while(i < len(data)):

        ## if the point is a boundary between slices. 
        ## UNIQUELY FOR SLICES.
        ## or if this is the end. we add what we have already
        if data[i][0] < tslice:
            newjson.append((tslice,vslice)) 
            tslice = get_lower_bound(data[i][0],slice)
            vslice = 0
            nb_points += 1


        ## if we have enough points,i.e. the window is full, for this period
        ## we pass to the next
        if nb_points == window:
           nb_points = 0
           period_count += 1
           if period_count >= nb_periods: return newjson ## finished !! do not go further
           next_ts = data[0][0] - period_count * period
           upbound,lowbound = get_next_period_slice_bounds(next_ts,slice)
           ## search for the upper bound of the slice
           while(i < len(data) and data[i][0] > upbound): i += 1
           if i == len(data) : return newjson; ##finished get out !!
           ## iterate while we still need to find a right ts.
           ## the right ts, might be several periods later, therefore we need to 
           ## for the next period each time we have an invalid ts
           while( not (data[i][0] <= upbound and data[i][0] >= lowbound)):
               ## there is a period missing, but we count it anyway
               period_count += 1
               ## we search for the counter-th period
               next_ts = data[0][0] - period_count * period
               upbound,lowbound = get_next_period_slice_bounds(next_ts,slice)
               ## search for the upper bound of the slice
               while(i < len(data) and data[i][0] > upbound): i += 1
               if i == len(data) : return newjson; ##finished get out !!
                          ## we're finally good here, we can go on
           ## first we sum the value before next_ts that belongs to the same slice
           while(i < len(data) and data[i][0] > next_ts):
               vslice += data[i][1]
               i += 1
           if i == len(data) : return newjson
           ## we are at the right ts !!!! i.e. the first ts of the next period
           ## update our var
           tslice = get_lower_bound(data[i][0],slice)
        ## we go to the next point 
        vslice += data[i][1]
        i += 1
        if i == len(data) : 
            newjson.append((tslice,vslice))
            break
    return newjson
          
            
           


def get_next_period_slice_bounds(next_ts,slice):
    """return the beginning and the end of the next slice in the next period"""
    ## next_upper_bound is the upper bound of the slice where next_ts fall i
    next_lower_bound = get_lower_bound(next_ts,slice)
    next_upper_bound = next_lower_bound + slice - 1 ## inclusive ==> -1
    return next_upper_bound,next_lower_bound



def get_lower_bound(ts,slice):
    return ts if ts % slice == 0 else ts - (ts % slice)

def get_upper_bound(ts,slice):
    return ts if ts % slice == 0 else ts + (slice - (ts % slice))

import unittest
from constants import *
from config import Config
import time
import json
import util
import controls
from parser import args
import main
class FormatterTest(unittest.TestCase):

    def test_format_data_empty_json(self):
        """Test formatting with an empty json"""
        Config.parse_file(DEFAULT_CONF_FILE)
        json = {}
        self.assertEqual(0,len(format_data(json,0,0,0,0)))
    def test_format_data_normal(self):
        """Test formatting with a fully filled json structure"""
        slice = 10*60 ## 10 MN
        window = 2 ## 2 points per period
        period = 3600 ## 1h / period
        nb_period = 2 ## total time = 2h
        data = FormatterTest.construct_data(unit=5*60,nb_period=3)
        nbpoints = len(data)
        util.pretty(data,output ="tty",text="NORMAL Before format : ")
        newdata = format_data(data,slice,period,nb_period,window)
        util.pretty(newdata,output="tty",text="NORMAL After format : ")
        self.assertEqual(window*nb_period,len(newdata))

    def test_format_slicing(self):
        """Test the format with slicing set to 2 and all the rest is ok.
        There are holes in the data, that the formatter must take care of"""
        slice = 2
        window = 1
        period = 2
        nb_periods = 10
        main.setup_logging()
        data = [
                (1422955984,100),(1422955984+1,100),
                (1422955984+4,100),(1422955984+5,100),
                (1422955984+8,100),(1422955984+9,100),
                (1422955984+12,10) ]
        data.reverse()
        pdata = format_data(data,slice,period,nb_periods,window)
        util.pretty(data,text = "SLICE Before format",output = "tty" )
        util.pretty(pdata,text = "SLICE After format",output = "tty")
        self.assertEqual(4,len(pdata))

    def test_format_slice_window(self):
        """Test the format with window set to 2 and same for slice and all the rest is ok.
        Holes in the data"""
        slice = 2
        window = 2
        period = 2
        nb_periods = 2
        main.setup_logging()
        data = [
                (1422955984,100),(1422955984+1,100),
                (1422955984+4,100),(1422955984+5,100),
                (1422955984+6,100),(1422955984+7,100),
                (1422955984+8,100),(1422955984+9,100),
                (1422955984+10,100),(1422955984+11,100),
                (1422955984+12,10) ]
        data.reverse()
        pdata = format_data(data,slice,period,nb_periods,window)
        util.pretty(data,text = "SLICE WINDOW Before format",output = "tty" )
        util.pretty(pdata,text = "SLICE WINDOW After format",output = "tty")
        self.assertEqual(window * nb_periods,len(pdata))
    @classmethod
    def construct_data(self,unit=60,period=3600,nb_period=3):
        """ Construct a sample json with a simple y=2x linear curve
        """
        count = 0
        ts = int(time.time())
        maxts = ts + nb_period * period
        data = []
        while ts < maxts:
            data.append((ts,count))
            count += 2
            ts += unit
        return list(reversed(data))



if __name__ == '__main__':
    unittest.main()
