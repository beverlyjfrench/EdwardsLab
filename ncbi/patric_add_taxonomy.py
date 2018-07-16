"""
Add the taxonomy to the patric metadata file
"""

import os
import sys
import argparse
from taxon import get_taxonomy_db, get_taxonomy

c = get_taxonomy_db()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Append taxonomy to the patric metadata file. This adds it at column 67")
    parser.add_argument('-f', help='patric metadata file', required=True)
    parser.add_argument('-o', help='output file', required=True)
    parser.add_argument('-t', help='taxonomy directory (or we will use default)')
    parser.add_argument('-v', help='verbose output', action="store_true")
    args = parser.parse_args()

    want = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']

    # read the file once to figure out the longest line
    maxp=0
    with open(args.f, 'r', encoding='utf-8') as f:
        for l in f:
            p = l.strip().split("\t")
            if len(p) > maxp:
                maxp = len(p)

    with open(args.o, 'w', encoding='utf-8') as out: 
        with open(args.f, 'r', encoding='utf-8') as f:
            for l in f:
                p = l.strip().split("\t")
                while (len(p) < maxp):
                    p.append("")

                if l.startswith("genome_id"):
                    out.write("{}\t{}\n".format(l.strip(), "\t".join(want)))
                    continue

                tid = p[3]

                level = {}

                t, n = get_taxonomy(tid, c)

                while t.parent > 1 and t.parent != 131567:
                    # 131567 is cellular organisms
                    if t.rank in want:
                        level[t.rank] = n.scientific_name
                    t, n = get_taxonomy(t.parent, c)

                for w in want:
                    if w in level:
                        p.append(level[w])
                    else:
                        p.append("")

                out.write("\t".join(p))
                out.write("\n")
