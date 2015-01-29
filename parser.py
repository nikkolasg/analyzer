import argparse
import constants as c
import dateutil.parser as parser
import datetime
def date(string):
    return parser.parse(string)

parser = argparse.ArgumentParser()
parser.add_argument("-v","--verbosity",help="verbosity level. Specify -v for INFO , -vv for DEBUG logging",action="count",default=c.DEFAULT_VERBOSE_LEVEL)
parser.add_argument("-c","--config",help="specify a config file.Default is config.json",type=str,default=c.DEFAULT_CONF_FILE)
parser.add_argument("-t","--timeref",help="Time Reference is the most recent time you want to analyze data. By default is the current time",type=date,default=datetime.datetime.now())
parser.add_argument("-g","--graphs",help="Generate graphs from reports into the graph folder",action="store_true")

args = parser.parse_args()

import unittest
class ParserTest(unittest.TestCase):

    def test_parser(self):
        pass

if __name__ == '__main__':
    unittest.main()
