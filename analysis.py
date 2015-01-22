import sys
import util
class Analysis:
    """ This class is used to describe an analysis we want to make.
    It is generally composed of a name (or id ),a source name (for now, later we may 
    implement a multi source analysis), some fields to analyze,
    with some conditions (for now Sql where clause statements)
    and an algorithm name, followed by options for this algorithm"""

    def __init__(self,name,sources,algorithm,window,slice,opts = {}):
        self.name = name
        self.sources = sources
        self.algorithm = algorithm
        self.window = window
        self.slice = slice
        ## options for the algorithm
        self.options = opts

    
    @classmethod
    def parse_json(self,json):
        """Read and set the corresponding members. Raise error if 
        found an aberration, or missing value"""
        if "name" not in json:
            print("No name specified in analysis part of json",file=sys.stderr)
            return None
        name = json["name"]
        if "sources" not in json: 
            print("No source name specified in analysis part of  json",file=sys.stderr)
            return None
        sources = util.listize(json["sources"])
        del json["sources"]

        if "algorithm" not in json:
            print("No algorithm specified in analysis part of json",file=sys.stderr)
            return None
        algorithm = json["algorithm"]
        del json["algorithm"]

        if "window" not in json:
            print("No window size specified in analysis part of json",file=sys.stderr)
            return None
        window = json["window"]

        if "slice" not in json:
            print("No slice size specified in analysis part of json",file=sys.stderr)
            return None
        slice = json["slice"]
        options = json.copy()

        return Analysis(name,sources,algorithm,window,slice,options)
        


