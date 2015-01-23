#!/usr/bin/env python3

import argparse
import logging as log
from config import Config
import constants as c

DEFAULT_CONF_FILE = "config.json"

parser = argparse.ArgumentParser()
parser.add_argument("-v","--verbosity",help="verbosity level. Specify -v,-vv,-vvv for different lelvel of verbosity",action="count",default=c.DEFAULT_VERBOSE_LEVEL)
    ## TODO
parser.add_argument("-c","--config",help="specify a config file.Default is config.json",type=str,default=c.DEFAULT_CONF_FILE)
args = parser.parse_args()

def setup_logging():
    """Setup the different logging handlers etc"""
    levels = { 0: log.DEBUG,
               1: log.INFO,
               2: log.WARNING,
               3: log.ERROR,
               4: log.CRITICAL}
    lvl = args.verbosity
    if lvl not in levels: lvl = c.DEFAULT_VERBOSE_LEVEL
    log.basicConfig(format="%(levelname)s\t%(asctime)s\t %(message)s",datefmt="%Y-%m-%d %H:%M",level=levels[lvl])

def credentials():
    return "Analysis tool v1.0 written in Python by nikkolasg & Jan De Liener."

def main():
    setup_logging()
    log.info(credentials())
    Config.parse_file(args.config)
    log.info("Application exiting ...")


if __name__ == '__main__':
    main()
     


