from math import ceil
from algorithm.generic import Generic
from report import Report
class Percentile(Generic):
    """Class that will label anomaly if above a specifed percentile"""
    def __init__(self,analysis,options = dict):
        Generic.__init__(self,analysis,options)

        self.percentile = float(options["percentile"]) if "percentile" in options else 95.0
        
        
    def run(self,json):
        for source,data in json.items():
            self.analyse(source,data)

    def analyse(self,source,data):
        def get_key(tu):
            return tu[1]
        report = self.analysis.report
        if len(data) < 2:
            report.store_message(Report.INFO,"Not enough data to analyse from {} for Percentile algorithm".format(source.name))

        new_ts,new_point = data[0][0],data[0][1]
        
        rank = ceil(len(data) * self.percentile / 100)
        low_ind = len(data) - rank if len(data) - rank >= 0 else 0
        up_ind = rank if rank < len(data) else len(data) - 1
        json_sorted = sorted(data, key=get_key)
        
        low_value = json_sorted[low_ind][1]
        up_value = json_sorted[up_ind][1]

        report.store_message(Report.DEBUG,"Percentile algorithm : new value = {}, normal intervals = [{},{}]".format(new_point,low_value,up_value))
        if new_point <= low_value:
            report.store_message(Report.ANOMALY,"Anomaly detected in source {} : new point ({}) below threshold {}.".format(source,new_point,low_value))
        elif new_point >= up_value:
            report.store_message(Report.ANOMALY,"Anomaly detected in source {} : new point ({}) above threshold {}.".format(source,new_point,up_value))
        
        else:
            report.store_message(Report.INFO,"No anomaly detected in source {}. All fine =)".format(source))
        
        

        
     
            
