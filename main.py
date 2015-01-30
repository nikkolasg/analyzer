#!/usr/bin/env python3

import argparse
import logging as log
from config import Config
import constants as c
from parser import args
import controls

def setup_logging():
    """Setup the different logging handlers etc"""
    levels = { 2: log.DEBUG,
               1: log.INFO}
    lvl = args.verbosity
    if lvl not in levels: lvl = c.DEFAULT_VERBOSE_LEVEL
    log.basicConfig(format="%(levelname)s\t%(asctime)s\t%(message)s",datefmt="%Y-%m-%d %H:%M",level=levels[lvl])

def credentials():
    return "Analysis tool v1.0 written in Python by nikkolasg & Jan De Liener."

def setup():
    setup_logging()
    log.info(credentials())
def cleanup():
    log.info("Application exiting ...")
def main():
    Config.parse_file(args.config)
    controls.run_all()


if __name__ == '__main__':
    setup()
    main()
    cleanup()
     


