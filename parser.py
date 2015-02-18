import argparse
import constants as c
import dateutil.parser as dparser
import datetime
import util
def date(string):
    try:
        ts = int(string)
        return util.ts2date(ts) ## yeah... we should catch exception if this is not
                                ## a good ts.................. boring
    except ValueError:
        ## this is a string date
        return dparser.parse(string)

parser = argparse.ArgumentParser()
parser.add_argument("-v","--verbosity",help="verbosity level. Specify -v for DEBUG logging",action="count",default=c.DEFAULT_VERBOSE_LEVEL)
parser.add_argument("-c","--config",help="specify a config file.Default is config.json",type=str,default=c.DEFAULT_CONF_FILE)
parser.add_argument("-t","--timeref",help="Time Reference is the most recent time you want to analyze data. By default is the current time",type=date,default=datetime.datetime.now())
parser.add_argument("-g","--graphs",help="Generate graphs from reports into the graph folder",action="store_true")
parser.add_argument("--analysis",help="If you only want to run a specfic analysis")
parser.add_argument("--noalert",help="Disable alert utility. useful for testing new data set.",action="store_true",default=False)
parser.add_argument("-d","--debug",help="Launch the PDB debugger interactive mode",action="store_true")

args = parser.parse_args()
import unittest
class ParserTest(unittest.TestCase):

    def test_parser(self):
        pass

if __name__ == '__main__':
    unittest.main()
