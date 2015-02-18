#!/usr/bin/env python3

from math import ceil,floor
from algorithm.generic import Generic
from report import Report
import util
import pdb
import logging as log
from parser import args

class Difference:
    """Class that implements methods to handle the computation of the difference
    of multiple sources, depending on the config"""
    def __init__(self,analysis,options = dict()):
        self.between = options["between"] if "between" in options else []
        self.iterator = iter(self.between)

        
    
    def get_next_difference(self,json):
        """Return the next difference to analyse"""
        try:
            assoc = self.get_next_assoc(json)
            s1 = json[assoc[0]]
            s2 = json[assoc[1]]
            diff_data = compute_difference(s1,s2)
            diff_name = compute_difference_name(assoc[0],assoc[1])
            log.debug("Difference Percentile Computation ({}):".format(diff_name))
            util.pretty(diff_data,"")
            return diff_name,diff_data
        except StopIteration:
            return None

    def get_next_assoc(self,json):
        """ Return the next valid association"""
        """ Can throw a stop iteration """
        assoc = next(self.iterator)
        while(assoc[0] not in json or assoc[1] not in json):
            log.debug("Association specified {} does not exist in json".format(assoc))
            assoc = next(self.iterator)
        return assoc



class Percentile(Generic):
    """Class that will label anomaly if above a specifed percentile"""
    """ 2 algorithms now : nearest, or linear"""
    LINEAR_THRESHOLD = 11 ## There must be at least 11 values to use the linear algo
                          ## See notes.
    def __init__(self,analysis,options = dict()):
        Generic.__init__(self,analysis,options)
        self.name = "Percentile algorithm"
        self.percentile = abs(float(options["percentile"])) if "percentile" in options else 95.0
        self.method = options["method"] if "method" in options else "nearest"
        self.scaling = abs(float(options["scaling"])) if "scaling" in options else 1
        self.delete_extremas = True if "delete_extremas" in options and options["delete_extremas"] == "true" else False 
        
    def run(self,json):
        for source,data in json.items():
            self.analyse(source,data)

    def analyse(self,source,data):
        report = self.analysis.report
        if len(data) < 3:
            report.store_message(Report.INFO,"Not enough data to analyse from {} for {}".format(source,self.name))
            return

        new_ts,new_point = data[0][0],data[0][1]
        if args.debug: pdb.set_trace()
        json_sorted = self.prepare_data(data)

        olow_value,oup_value = self.compute_percentile_endpoints(json_sorted) 
        
        ## we scale to allow new value. if scale = 1 (default) no new values
        low_value,up_value = self.scale(olow_value,oup_value)

        report.store_message(Report.DEBUG,"{} (for {}): new value = {}, normal intervals = [{},{}] (before scale:[{},{}]".format(self.name,source,new_point,low_value,up_value,olow_value,oup_value))
        self.check_new_point(report,source,new_point,up_value,low_value)
        

    def check_new_point(self,report,source,new_point,up_value,low_value):
        """Check the values and sends to the report if needed"""
        if new_point < low_value:
            report.store_message(Report.ANOMALY,"Anomaly detected in source {} : new point ({}) below threshold {}.".format(source,new_point,low_value))
        elif new_point > up_value:
            report.store_message(Report.ANOMALY,"Anomaly d  etected in source {} : new point ({}) above threshold {}.".format(source,new_point,up_value))
        
        else:
            report.store_message(Report.INFO,"No anomaly detected in source {}. All fine =)".format(source))
       

    def prepare_data(self,json):
        def get_key(tu):
            return tu[1]
        del json[0]
        json = sorted(json,key = get_key)
        if self.delete_extremas is not True: return json
        del json[0]
        del json[-1]
        return json

    def scale(self,low_value,up_value):
        """WIll scale the interval specified by the 2 endpoints by the scaling factor. Basically split the difference between before and after to the endpoints"""
        interval = up_value - low_value
        ninterval = interval * self.scaling
        low_value = low_value - (ninterval - interval) 
        if low_value < 0 : low_value = 0
        up_value = up_value + (ninterval - interval)
        return (low_value,up_value)


    def compute_percentile_endpoints(self,json):
        """ Compute the endpoints for a given percentile over the given json data.
        Depending on the options, either nearest rank method, or linear interpolation closest rank method."""
        if self.method == "linear" and len(json) > 10:
            return self.compute_linear_percentile_endpoints(json)
        else: ## by defaut the nearest method
            if len(json) < 10: log.info("Percentile will use the nearest instead of the linear algorithm due to the lack of data (there must be at least 11).")
            return self.compute_nearest_percentile_endpoints(json)

    ######### NOTES ##########
    ## if less than 11 datas, outliners will not be discarded iwth a 90% percentile
    ## because at 10, it will make linear interpolation between the before last
    ## and the last (supposed it is the outliner,exemple 1 January). 
    ## so the interpolated value will be large.
    def compute_linear_percentile_endpoints(self,json):
        """according to the linear interpolation between closest rank method from wikipedia"""
        """Return the low index and upper index """
        def nth_percent(index): return (100/len(json)) * (index - 0.5)
        def interpolation(low,up,percentile):
            lvalue = json[low-1][1]
            uvalue = json[up-1][1]
            return lvalue + len(json) * (percentile - nth_percent(low)) * (uvalue - lvalue) / 100

        length = len(json)
        nth_value = (self.percentile * length / 100) + 0.5
        ## If it is an integer, that means we get right on a existing number
        if util.isInteger(nth_value):
            low = length - nth_value - 1 if length - nth_value -1 > 0 else 0
            up = nth_value - 1 if nth_value - 1 > 0 and nth_value - 1 < length else length - 1
            return (json[int(low)][1],json[int(up)][1])

        ## else we got multiple choices
        ## lambda taht compute percentile for a given rank (nth_value)
        first_perc,last_perc = nth_percent(1),nth_percent(length)
        if self.percentile < first_perc or self.percentile > last_perc:
            return (json[0][1],json[length-1][1])

        #interpolation
        low_idx,up_idx = floor(nth_value),ceil(nth_value)
        ## > strict because we talks about nth_value, which has a 1-offset contrary to 0-offset python list
        if low_idx < 1 or low_idx > length or up_idx < 1 or up_idx > length: 
            log.error("Percentile given is erronous. ({} ==> length = {}, nth_value = {}, indx [{},{}]. Abort".format(self.percentile,length,nth_value,low_idx,up_idx))
            raise ValueError("Percentile Given is erronous. Abort")

        up_interpol = interpolation(low_idx,up_idx,self.percentile)
        low_interpol = interpolation(length - up_idx + 1,length - low_idx + 1,100-self.percentile) 
        
        return (low_interpol,up_interpol)
         
    def compute_nearest_percentile_endpoints(self,data):
        ##nearest rank method 
        urank = floor(len(data) * self.percentile / 100)
        lrank = ceil(len(data) * (100 - self.percentile) / 100)
        low_ind = lrank - 1 if lrank > 0 else 0
        up_ind = urank - 1 if urank < len(data) and urank > 0 else len(data) - 1
        return (data[low_ind][1],data[up_ind][1]) 


from processor import *

class DifferencePercentile(Percentile,Difference):
    """Same as percentile class, only that it computes the difference between two
    and analyse this data"""
    def __init__(self,analysis,options = dict()):
        Percentile.__init__(self,analysis,options)
        Difference.__init__(self,analysis,options)
        self.name = "Difference Percentile Algorithm"
    
    def run(self,json):
        """Compute the difference between the two sources"""
        if len(json) < 2:
            self.analysis.report.store_message(Report.INFO,"Difference Percentile has not received enough data. Abort.")
            return
        if args.debug: pdb.set_trace()
        assoc = self.get_next_difference(json)
        while(assoc is not None):
            self.analyse(*assoc)
            assoc = self.get_next_difference(json)


class StandardDeviationPercentile(Percentile):
    """Use the Percentile Algorithm to get its data, then perform a
    simple mean / std dev, then check if new value goes out of bound.
    Bounds are [mean - 3 * stddev, mean + 3 * stddev] by default.
    the '3' is a variable and can be changed by specifying a 
    sigma_rule option in the config.Can be a float"""
    def __init__(self,anaylsis,options = dict()):    
        Percentile.__init__(self,anaylsis,options)
        self.name = "Standard Deviation - Percentile Based"
        self.sigma_rule = abs(float(options["sigma_rule"])) if "sigma_rule" in options else 3

    def run(self,json):
        for source,data in json.items():
            self.analyse(source,data)

    def analyse(self,source,data):
        """ see Percentile class abose for more details"""
        report = self.analysis.report
        if len(data) < 3:
            report.store_message(Report.INFO,"{} : Not enough data to analyse from {}".format(self.name,source))
            return

        new_ts,new_point = data[0][0],data[0][1]
        
        if args.debug: pdb.set_trace()
        json_sorted = self.prepare_data(data)

        olow_value,oup_value = self.compute_percentile_endpoints(json_sorted)
        ## newjson keeps the value from the json that are IN the interval
        ## it will be used to compute the mean & stddev
        new_json = [ (time,value) for time,value in json_sorted if value >= olow_value and value <= oup_value ]
        ## make the stats
        mean = compute_mean(new_json)
        std_dev = compute_std_dev(new_json,mean)
        ## This is the final limit interval
        low_value = mean - self.sigma_rule * std_dev
        up_value = mean + self.sigma_rule * std_dev

        report.store_message(Report.DEBUG,"{} ({}): new point = {}, percentile [{},{}], mean = {}, dev = {}, interval [{},{}]".format(self.name,source,new_point,olow_value,oup_value,mean,std_dev,low_value,up_value))

        self.check_new_point(report,source,new_point,up_value,low_value)

class DifferenceStandardDeviationPercentile(StandardDeviationPercentile,Difference):
    """Used for compute the ratio between two sources uzsing the Standard Deviation Percentile algorithm"""
    def __init__(self,analysis,options = dict()):
        StandardDeviationPercentile.__init__(self,analysis,options)
        Difference.__init__(self,analysis,options)
        self.name = "Difference Standard Deviation Percentile Algorithm"
    
    def run(self,json):
        """Compute the difference between the two sources"""
        if len(json) < 3:
            self.analysis.report.store_message(Report.INFO,"{} has not received enough data. Abort.".format(self.name))
            return
        if args.debug: pdb.set_trace()
        assoc = self.get_next_difference(json)
        while(assoc is not None):
            self.analyse(*assoc)
            assoc = self.get_next_difference(json)
