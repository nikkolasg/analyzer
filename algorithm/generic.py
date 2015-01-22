class Generic:
    """ Represent base class of any algorithm to implement"""
    def __init__(self,options = dict):
        self.message = ""
        self.options = options

    def analyze(json):
        raise NotImplementedError("Subclass must implement analyze function.")

    def __str__(self):
        return "Algorithm decsription : "

        
