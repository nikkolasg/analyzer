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
        new_point = data[0][1]
        avg = 0
        count = 0 
        ## we dont take the first point as this is the point to analyse. and we do 
        ## not need to take the "windows" point for this algorithm
        i = self.analysis.window
        window = self.analysis.window
        while ( i < len(data) ):
            avg += data[i][1]
            count += 1
            i += window 
        
        avg /= count if count != 0 else 1
        low,up = self.bounds(avg)
        self.analysis.report.store(Report.INFO,"Simple Average : new value = {}, average = {} & {} threshold ==> [{},{}]".format(new_point,avg,self.threshold,low,up))
        if new_point < low:
            self.analysis.report.store(Report.ERROR,"Anomaly Detected in source {}: new point {} on {} is below threshold!".format(source,data[0][1],util.ts2date(data[0][0])))
        elif new_point > up:
            self.analysis.report.store(Report.ERROR,"Anomaly Detected in source {}: new point {} on {} is above trheshold!".format(source,data[0][1],util.ts2date(data[0][0])))
        else:
            self.analysis.report.store(Report.INFO,"No anomaly detected in source {}. All fine =)".format(source))

    def bounds(self,average):
        """Return simple calculated interval for a average value """
        return (int(average - average * self.threshold),int(average + average * self.threshold))
        


