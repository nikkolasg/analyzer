import datetime as d

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

class Singleton(type):
    instance = None
    def __call__(cls,*args,**kargs):
        if not cls.instance:
            cls.instance = super(Singleton,cls).__call__(*args,**kargs)
        return cls.instance
