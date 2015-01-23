""" This module format a JSON according to come criterion in a analysis.
Specifically, it will slice the original data, take #window points for each periods
"""
import logging as log

def format(json, analysis):
    newjson = {}
    for source_name,data in json:
        newjson[source_name] = format_data(data,analysis) 

    return newjson

def format_data(data,analysis):
    """Responsible for doing the slicing / windowing / perioding operations """
    newjson = []
    if len(data) < 1: 
        log.debug("No data to format ...")
        return newjson
    i = 0 ## we suppose the first entry is the most recent one
    tslice = get_lower_bound(data[islice],analysis.slice) 
    vslice = 0 ## value summing all values in a slice
    nbperiod = 0 ## how many periods have we done yet
    nbwindow = 0 ## how many points have we taken by periodsd
    good_index = 0 ## the last point that falls exactly on our period. Use it to get the next good_index, like good_index - analysis.period
    while(i < len(data)):
        ## if wa have crossed a slice boundary, insert the value
        ## of the slice we computed into the new json
        if data[i] < tslice:
            data.append((tslice,vslice))
            tslice = get_lower_bound(data[i])
            vslice = 0
            nbwindow += 1

        ## if we have sliced enough point for a week or a month(for a period),
        ## we gonna search to the precedent starting period directly
        if nbwindow == analysis.window:
            nbwindow = 0
            nbperiod += 1
            ## we have analyzed enough data, stop !
            if nbperiod > analysis.nb_periods: break
            ## this is the next timestamp that begins a new period
            next_ts = data[good_index] - analysis.period
            ## we take the upper bound of the precedent period
            ## that way any point before the exact precedent period starting point
            ## that may fall down under the SAME slice, will be evaluated
            next_bound = get_upper_bound(next_ts)
            ## iterate as long as we dont find a goog point
            while(data[i] > next_bound and i < len(data)): i += 1
            if i == len(data): break
            
            while(data[i] > next_ts and i < len(data)): 
                ## store the preceding values falling down under the same slice
                vslice += data[i]
                i += 1
            good_index = i
            tslice = get_lower_bound(data[i]) ## same for the slice 
        
        vslice += data[i]

        

def get_lower_bound(timest,slice):
    """Return the lower bound of time formatted by the slice var from the Epoch.
    i.e. if slice = 3600, timest = 3h15 ==> timest = 3h00"""
    return timest - (timest % slice)
        
def get_upper_bound(timest,slice):
    """Same as lower_bound except return the upper bound ...;) """
    return timest + (timest % slice)
