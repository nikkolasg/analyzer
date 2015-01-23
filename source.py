import sys
import logging as log
class Source:
    """This class is used to represent a source,i.e. data in a table, filtered
    by somes clauses and only for certain fields. It takes a name (just for simplicity),table name,a where_clause, and a fields clause."""
    def __init__(self,name,table,where_clause):
        self.name = name
        self.table = table
        self.where_clause = where_clause

    @classmethod
    def parse_json(self,json):
        """Read ans set appropriate members of source class"""
        if "name" not in json: 
            log.warning("Name part is not present in the Source part of json",file=sys.stderr)
            return None
        name = json["name"]

        if "table" not in json:
            log.warning("Table part is not present in the Source part of json",file=sys.stderr)
            return None
        table = json["table"]
        
        where_clause = json["where_clause"] if "where_clause" in json else ""
        return Source(name,table,where_clause)

