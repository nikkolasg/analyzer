import argparse
import constants as c
import dateutil.parser as parser
def date(string):
    return parser.parse(string)

parser = argparse.ArgumentParser()
parser.add_argument("-v","--verbosity",help="verbosity level. Specify -v,-vv,-vvv for different lelvel of verbosity",action="count",default=c.DEFAULT_VERBOSE_LEVEL)
parser.add_argument("-c","--config",help="specify a config file.Default is config.json",type=str,default=c.DEFAULT_CONF_FILE)
parser.add_argument("-t","--timeref",help="Time Reference is the most recent time you want to analyze data. By default is the current time",type=date)

args = parser.parse_args()
