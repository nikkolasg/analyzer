import datetime as d
import logging as log
import math
def listize(obj):
    if isinstance(obj,str): return [obj]
    return obj


def pprint_data(json):
    """Pretty print the data in json format [ (ts,value),(ts,value) ...]
    will output date,value
    """
    for ts,value in json:
        print(ts2str(ts) + " -> " + str(value))
    
def ts2str(ts):
    return str(d.datetime.fromtimestamp(ts))
def ts2date(ts):
    return d.datetime.fromtimestamp(ts)
def now2str():
    return d.datetime.now().strftime("%Y%m%d%H%M%S")

def pretty(json,text = "JSON",output = "log" ):
    """Print in a pretty manner the json returned by format (only for one source)
    You can specify a header text , and the output method (if you specify
    stg else as 'log' it will be print on the screen"""
    m = log.debug if output == "log" else print
    if isinstance(json,list):
        m("*" * 50)
        m(text)
        print_data(json,m)
    else:
        for source,data in json.items():
            m("*" * 50)
            m(text + " (source = {}) : ".format(source))
            print_data(data,m)

def print_data(data,method):
    count = 0
    s = ""
    for ts,value in data:
        s += "({} => {})\t".format(ts2str(ts),value)
        count += 1
        if count % 4 == 0: 
            method(s)
            s = ""
    if not count % 4 == 0: 
        method(s)


def isInteger(number):
    """Return true if this is an integer, false if it is a real number"""
    return number == math.floor(number)

class Singleton(type):
    instance = None
    def __call__(cls,*args,**kargs):
        if not cls.instance:
            cls.instance = super(Singleton,cls).__call__(*args,**kargs)
        return cls.instance
