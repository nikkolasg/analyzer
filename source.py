#!/usr/bin/env python3
import unittest

class Source:
    """This class contains infos about the definition of a table
    where to fetch the data. Essentially you must specify some fields.
    The table here must be in the format :
    timestamp, type1 (type2, etc), counter1, (counter 2, etc) """

    def __init__(self):
        self.time_field = ""
        self.fields = list
        self.table = ""
        self.name = ""

    def parse_json(self,json):
        """set the corresponding members from the json
        to this object. Raise an error if any values is not adequate
        or there is not enough data"""
        if "name" not in json: raise NameError("No name present in the source json part")
        self.name = json["name"]
        
        if "table" not in json: raise NameError("No table present in the source json part")
        self.table = json["table"]

        if "time_field" not in json: raise NameError("No time field present in the source json part")
        self.time_field = json["time_field"]

        if "fields" not in json: raise NameError("No fields present in the source json part")
        self.fields = json["fields"]

    def __str__(self):
        return """Name : {}  
              Table : {} 
              Time field : {}
              Fields : {}""".format(self.name,self.table,self.time_field,str(self.fields))


class SourceTest(unittest.TestCase):

    def test_parse_json(self):
        source = Source()
        self.assertRaises(NameError,source.parse_json,{})
        json = { "name": "udr_stats","table":"udr",
                "time_field":"timest","fields": ["proto","category"]}
        source.parse_json(json)
        self.assertTrue("udr" in str(source))

if __name__ == '__main__':
    unittest.main()

        
