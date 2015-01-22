#!/usr/bin/env python3
import unittest
import sys
class Table:
    """This class contains infos about the definition of a table_name
    where to fetch the data. Essentially you must specify some fields.
    The table here must be in the format :
    timestamp, type1 (type2, etc), counter1, (counter 2, etc) """

    def __init__(self,name,table_name,database,time_field,fields):
        self.time_field = time_field
        self.fields = fields
        self.table_name = table_name
        self.name = name
        self.database = database
    
    @classmethod
    def parse_json(self,json):
        """set the corresponding members from the json
        to this object. Raise an error if any values is not adequate
        or there is not enough data"""
        
        if "name" not in json: 
            print("No name present in the table json part",file=sys.stderr)
            return None
        name = json["name"]
        
        if "table_name" not in json: 
            print("No table_name present in the table json part",file=sys.stderr)
            return None
        table_name = json["table_name"]

        if "time_field" not in json: 
            print("No time field present in the table json part",file=sys.stderr)
            return None
        time_field = json["time_field"]

        if "fields" not in json: 
            print("No fields present in the table json part",file=sys.stderr)
            return None
        fields = json["fields"]

        if "database" not in json: 
            print("No database field present in the table json part",file=sys.stderr)
            return None
        database = json["database"]
        return Table(name,table_name,database,time_field,fields)


    def __str__(self):
        return """Name : {}  
              Table : {} 
              Time field : {}
              Fields : {}""".format(self.name,self.table_name,self.time_field,str(self.fields))


class TableTest(unittest.TestCase):

    def test_parse_json(self):
        """Simple parsing json test"""
        table = Table()
        self.assertIsNone(table.parse_json({}))
        json = { "name": "udr_stats","table_name":"udr",
                "time_field":"timest","fields": ["proto","category"]}
        table.parse_json(json)
        self.assertTrue("udr" in str(table))

if __name__ == '__main__':
    unittest.main()

        
