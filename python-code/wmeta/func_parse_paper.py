# -*- coding: utf-8 -*-

import os
import re
import csv
import json

def parse_paper_csv(filename):
    if not os.path.exists(filename):
        print "file not exists ", filename
        return

    map_author = {}
    list_paper = []
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            v1 =  row["All author's Emails"].split(";")
            v2 = row["All Author Full Names with Main Affiliation"].split(";")
            if len(v1) != len(v2):
                print len(v1),len(v2), v1, v2





filename = "WWW2015ResearchPapers.csv"
dir_home = os.path.dirname(os.path.dirname(__file__))
filename = os.path.join(dir_home, "data/raw", filename)
parse_paper_csv(filename)