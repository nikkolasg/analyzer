from report import Report
import logging as log
class Generic:
    """ Represent base class of any algorithm to implement"""
    def __init__(self,analysis,options = dict):
        self.options = options
        self.analysis = analysis

    def run(self,json):
        raise NotImplementedError("Subclass must implement analyze function.")

    def __str__(self):
        return "Algorithm decsription : "
    
    def rapport(self):
        return self.messages
        

import util

class SimpleAverage(Generic):
    """ Simple average algorithm where it takes the average of the precedent values
    and compare it to the most recent one. It removes the values from
    the highest and lowest point. and may have different threshold for the upper 
    and lower bound"""

    def __init__(self,analysis,options = dict):
        Generic.__init__(self,analysis,options)
        if "threshold" in options:
            self.upper_threshold = self.lower_threshold = float(options["threshold"])
        elif "upper_threshold" in options and "lower_threshold" in options:
            self.upper_threshold = float(options["upper_threshold"])
            self.lower_threshold = float(options["lower_threshold"])
        else:
            self.upper_threshold = self.lower_threshold = 0.3
        if "delete_extremes" in options:
            if options["delete_extremes"] in ["true","True",1,"1"]: self.delete_extremes = True
            else: self.delete_extremes = False
        else:
            self.delete_extremes = False
            
        self.threshold = float(options["threshold"]) if "threshold" in options else 0.5


    def run(self,json):
        """ Main method to call, will run the algorithm for each sources"""
        for source,data in json.items():
            self.analyse(source,data)

    def analyse(self,source,data):
        """ The algorithm it self for one source / data pair"""
        report = self.analysis.report
        if len(data) < 2:
            report.store_message(Report.INFO,"Not enough data to analyse from {} for SimpleAverage algorithm".format(source.name))
            return
        ## will contains the value USED by the algorthm and therefor the values
        ## to display
        graph = []
        min_ts = data[0][0]
        max_ts = data[len(data)-1][0]
        
        new_point = data[0][1]
        ## let's keep track of the min & max so we can remove them after
        ## so keep the value & the index in the json
        min_value = max_value = (min_ts,new_point) 
        avg = 0
        count = 0 
        ## we dont take the first point as this is the point to analyse. and we do 
        ## not need to take the "windows" point for this algorithm
        i = self.analysis.window
        window = self.analysis.window
        while ( i < len(data) ):
            avg += data[i][1]
            graph.append([data[i][0],data[i][1]])
            if min_value[1] > data[i][1]: min_value = (data[i][0],data[i][1])
            if max_value[1] < data[i][1]: max_value = (data[i][0],data[i][1])
            count += 1
            i += window 
       
        ## we eliminate the extrems
        if self.delete_extremes:
            graph.remove(min_value)
            graph.remove(max_value)
            ## then compute avg
            avg -= (min_value + max_value)
            count -= 2

        avg /= count if count != 0 else 1
        ## Upper and lower bounds that defines if a point is "normal" or not
        low,up = self.bounds(avg)

        report.store_message(Report.DEBUG,"Simple Average : new value = {}, average = {} (for {} values) & {} threshold ==> [{},{}]".format(new_point,int(avg),count,self.threshold,low,up))
        if new_point < low:
            report.store_message(Report.ANOMALY,"Anomaly Detected in source {}: new point value {} on {} is below threshold!".format(source,data[0][1],util.ts2str(data[0][0])))
        elif new_point > up:
            report.store_message(Report.ANOMALY,"Anomaly Detected in source {}: new point value {} on {} is above trheshold!".format(source,data[0][1],util.ts2str(data[0][0])))

        else:
            report.store_message(Report.INFO,"No anomaly detected in source {}. All fine =)".format(source))

        report.add_curve("Simple Average {}".format(source),"data",graph)
        report.add_curve("Simple Average {}".format(source),"average",[[min_ts,avg],[max_ts,avg]])
        report.add_curve("Simple Average {}".format(source),"upper bound",[[min_ts,up],[max_ts,up]])
        report.add_curve("Simple Average {}".format(source),"lower bound",[[min_ts,low],[max_ts,low]])

    def bounds(self,average):
        """Return simple calculated interval for a average value """
        return (int(average - average * self.lower_threshold),int(average + average * self.upper_threshold))
        


