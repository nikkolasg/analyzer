from report import Report
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
    and compare it to the most recent one"""

    def __init__(self,analysis,options = dict):
        Generic.__init__(self,analysis,options)
        self.threshold = float(options["threshold"]) if "threshold" in options else 0.5

    def run(self,json):
        """ Main method to call, will run the algorithm for each sources"""
        for source,data in json.items():
            self.analyse(source,data)

    def analyse(self,source,data):
        """ The algorithm it self for one source / data pair"""
        if len(data) < 2:
            log.warning("Not enough data to analyse from {} for SimpleAverage algorithm".format(source))
            return
        report = self.analysis.report
        graph = []
        min_ts = data[0][0]
        max_ts = data[len(data)-1][0]

        new_point = data[0][1]
        avg = 0
        count = 0 
        ## we dont take the first point as this is the point to analyse. and we do 
        ## not need to take the "windows" point for this algorithm
        i = self.analysis.window
        window = self.analysis.window
        while ( i < len(data) ):
            avg += data[i][1]
            graph.append([data[i][0],data[i][1]])
            count += 1
            i += window 
        
        avg /= count if count != 0 else 1
        low,up = self.bounds(avg)
        report.store_message(Report.INFO,"Simple Average : new value = {}, average = {} (for {} values) & {} threshold ==> [{},{}]".format(new_point,int(avg),count,self.threshold,low,up))
        if new_point < low:
            report.store_message(Report.ERROR,"Anomaly Detected in source {}: new point {} on {} is below threshold!".format(source,data[0][1],util.ts2str(data[0][0])))
        elif new_point > up:
            report.store_message(Report.ERROR,"Anomaly Detected in source {}: new point {} on {} is above trheshold!".format(source,data[0][1],util.ts2str(data[0][0])))
        else:
            report.store_message(Report.INFO,"No anomaly detected in source {}. All fine =)".format(source))

        report.add_curve("Simple Average","data",graph)
        report.add_curve("Simple Average","average",[[min_ts,avg],[max_ts,avg]])
        report.add_curve("Simple Average","upper bound",[[min_ts,up],[max_ts,up]])
        report.add_curve("Simple Average","lower bound",[[min_ts,low],[max_ts,low]])

    def bounds(self,average):
        """Return simple calculated interval for a average value """
        return (int(average - average * self.threshold),int(average + average * self.threshold))
        


