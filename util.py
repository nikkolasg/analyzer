import datetime as d

def listize(obj):
    if isinstance(obj,str): return [obj]
    return obj


def pprint_data(json):
    """Pretty print the data in json format [ (ts,value),(ts,value) ...]
    will output date,value
    """
    for ts,value in json:
        print(ts2date(ts) + " -> " + str(value))
    
def ts2date(ts):
    return str(d.datetime.fromtimestamp(ts))
