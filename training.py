#!/usr/bin/env python3
import mysql.connector
from mysql.connector import errorcode
import contextlib
import sys

def func_keywords(a="aaa",b="bbb",c="ccc"):
    print("a = {}, b = {}, c = {}".format(a,b,c))

json = {
        "a" : "nopeA",
        "b" : "nopeB"
        }
func_keywords(**json)
func_keywords(a="insidecall")

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-o","--option",help="set an optional value")
args = parser.parse_args()
if args.option:
    print("Optional value : {}".format(args.option))
else:
    print("No optional value passed...")

