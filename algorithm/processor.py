#!/usr/bin/env python3
"""Contains a lot of utility method for processing data for algorithms.
Like difference, mean , std deviation etc """
from math import sqrt
def compute_difference(source1,source2):
    """Compute the difference between two sources. 
    You may change this class if you want different behavior when
    there is difference in timestamp, they may not be a one-to-one mapping
    between the timestamps. Here we skip. You could replace by a default value etc"""
    timestamps = list()
    ## take all the from the first source and make it a dict
    tmp = dict(source1)
    ## compute the final list by iterating over the second list 
    for time,value in source2:
        if time in tmp: timestamps.append((time, tmp[time]-value))

    return timestamps

def compute_difference_name(source1,source2):
    return "diff_" + source1 + "_" + source2

def compute_mean(json,out = int):
    """Compute the mean of one time series.Do not pass data from multiple source!"""
    mean = 0
    for time,value in json:
        mean += value
    return out(mean/len(json))

def compute_std_dev(json,mean = None,out = int):
    """There are some formulas to compute at the stddev in one pass without the mean    but there are problemes with big numbers and is not easy implementable.
    For ease of simplicity, we just do it in 2 passes, but might change later"""
    mean = compute_mean(json) if mean is None else mean
    stddev = 0
    for time,value in json:
        stddev += (mean - value) ** 2
    return out(sqrt(stddev/len(json)))

import unittest

class ProcessorTest(unittest.TestCase):

    def test_difference_json(self):
        j = { "source1" : 
                [ (1,1),
                   (2,2),
                   (4,4),
                   (5,5)
                   ],
                "source2":
                [   (1,1),
                    (3,3),
                    (4,4),
                    (5,5),
                    (8,8)
                ]
            }
        diff = [ (1,0),(4,0),(5,0) ]
        ## multiple names because we dont use ordered dict
        names = ["diff_source1_source2","diff_source2_source1"]
        actual_diff = compute_difference(j)
        self.assertEqual(diff,actual_diff)
        actual_name = compute_difference_name(j)
        self.assertTrue(actual_name in names)
 
if __name__ == '__main__':
     unittest.main()
