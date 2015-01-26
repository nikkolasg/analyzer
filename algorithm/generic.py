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
        self.threshold = int(options["threshold"]) if "threshold" in options else 0.5

    def run(self,json):
        """ Main method to call, will run the algorithm for each sources"""
        for source,data in json:
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
            i += window - 1
        
        avg /= count
        low,up = self.bounds(avg)
        if new_point < low:
            analysis.report.store(Report.ERROR,"Anomaly Detected in source {}: new point {} on {} is below threshold!".format(source,*data[0]))
        elif new_point > up:
            analysis.report.store(Report.ERROR,"Anomaly Detected in source {}: new point {} on {} is above trheshold!".format(source,*data[0]))
        else:
            analysis.report.store(Report.INFO,"No anomaly detected in source {}. All fine =)".format(source))

    def bounds(self,average):
        """Return simple calculated interval for a average value """
        return (average + average * self.threshold,average - average * self.threshold)
        


