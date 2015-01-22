import sys
class Source:
    """This class is used to represent a source,i.e. data in a table, filtered
    by somes clauses and only for certain fields. It takes a name (just for simplicity),table name,a where_clause, and a fields clause."""
    def __init__(self):
        self.name = ""
        self.table = ""
        self.where_clause = ""
        self.fields = []

    @classmethod
    def parse_json(self,json):
        """Read ans set appropriate members of source class"""
        s = Source()
        if "name" not in json: 
            print("Name part is not present in the Source part of json",file=sys.stderr)
            return None
        s.name = json["name"]

        if "table" not in json:
            print("Table part is not present in the Source part of json",file=sys.stderr)
            return None
        s.table = json["table"]
        
        if "fields" not in json:
            print("Fields part is not present in the source part of json",file=sys.stderr)
            return None
        s.fields = json["fields"]
        
        if "where_clause" in json: s.where_clause = json["where_clause"]
        return s

