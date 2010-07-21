#!/usr/bin/env python
from ruffus import *
import sys

def first_task():
    print "First task"

@follows(first_task)
def second_task():
    print "Second task"

@follows(second_task)
def final_task():
    print "Final task"
pipeline_printout_graph ( "manual_follows1.png",
                         "png",
                         [final_task],
                         no_key_legend=True)

