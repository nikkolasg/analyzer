class Analyze:
    """ This class is used to describe an analysis we want to make.
    It is generally composed of a name (or id ),a source name (for now, later we may 
    implement a multi source analysis), some fields to analyze,
    with some conditions (for now Sql where clause statements)
    and an algorithm name, followed by options for this algorithm"""

    def __init__(self):
        self.name = ""
        self.source = None
        self.where_clause = ""
        self.columns = []
        self.algorithm = None
        ## options for the algorithm
        self.options = dict

    def parse_json(self,json):
        """Read and set the corresponding members. Raise error if 
        found an aberration, or missing value"""
        if "source" not in json: raise NameError("No source name specified in json")


