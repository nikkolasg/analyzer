#!/usr/bin/env python3

import argparse
import logging as log
from config import Config
import constants as c
from parser import args


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
     


