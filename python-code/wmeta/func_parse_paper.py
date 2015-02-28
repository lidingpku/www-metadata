# -*- coding: utf-8 -*-

import os
import re
import csv
import json
from operator import itemgetter, attrgetter, methodcaller



def parse_paper_csv(filename):
    print "processing ", filename

    if not os.path.exists(filename):
        print "file not exists "
        return



    map_author = {}
    map_author_paper = {}
    list_paper = []
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            # align author
            v1 = [x.strip() for x in row["All author's Emails"].split(";")]
            v2 = [x.strip() for x in row["All Author Full Names with Main Affiliation"].split(";")]
            if len(v1) != len(v2):
                print "ERROR", len(v1),len(v2), v1, v2
                exit(1)
            else:


                list_author = []
                for (email,author) in zip(v1,v2):
                    v3 = [x.strip() for x in re.split(r"[\(\)]", author)]
                    family_name = v3[0].split(" ")[-1]

                    map_author_paper[email] = map_author_paper.get(email,[])
                    map_author_paper[email].append(row["Paper ID (from EasyChair)"])


                    author = {
                        "name": v3[0],
                        "family_name": family_name,
                        "affiliation":v3[1],
                        "email": email,
                        "paper_count": len(map_author_paper[email]),
                        "paper_ids": ";".join(map_author_paper[email])
                    }
                    list_author.append(author)
                    map_author[email] = author

                    #sprint author

            #print row
            paper = {
                "paper_id": row["Paper ID (from EasyChair)"],
                "paper_type": row["Paper type"],
                "title": row["Title"],
                "authors": [x["name"] for x in list_author],
                "authors_email": [x["email"] for x in list_author]
            }
            list_paper.append(paper)

    #with open(filename_output,"w") as f:
    print json.dumps(list_paper, ensure_ascii=False, indent=4)
    filename_output = os.path.join(dir_home, "data/output", "research_paper.json")
    with open(filename_output, "w") as f:
        json.dump(list_paper,f, ensure_ascii=False, indent=4)

    temp = sorted(map_author.values(), key=itemgetter("family_name"))
    #print json.dumps(temp, ensure_ascii=False, indent=4, sort_keys=True)

    filename_output = os.path.join(dir_home, "data/output", "research_author.csv")
    with open(filename_output, "w") as f:

        w = csv.DictWriter(f, ["name","affiliation","email","family_name","paper_ids","paper_count"])
        w.writeheader()
        for author in temp:
            w.writerow(author)

    print len(list_paper), len(map_author)

    print json.dumps(map_author_paper, ensure_ascii=False, indent=4, sort_keys=True)


filename = "WWW2015ResearchPapers.csv"
dir_home = os.path.dirname(os.path.dirname(__file__))
filename = os.path.join(dir_home, "data/raw", filename)

parse_paper_csv(filename)