import generic
import util

class HistoryAverage(Generic):

    def __init__(self,analysis,options = dict):
        Generic.__init__(self,anaylsis,options)
        if "threshold" in options:
            self.upper_threshold = self.lower_threshold = options["threshold"]
        elif "upper_threshold" in options and "lower_threshold" in options:
            self.upper_threshold = options["upper_threshold"]
            self.lower_threshold = options["lower_threshold"]
        else
            self.upper_threshold = self.lower_threshold = 0.3

    def run(self,json):
        """main method ;) """
        pass
