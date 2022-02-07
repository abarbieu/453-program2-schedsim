import sys
import numpy as np
import argparse

def readAssign(file):
    f = open(file)
    for l in f.readlines():
        print(np.array(l.strip('\n').split(' '),dtype=int))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deal with jobs.txt -q and -p')
    parser.add_argument("jobfile")
    parser.add_argument(
        "-q",
        default=1,
        help="optional time quantile for round robin, default: 1")

    parser.add_argument(
        "-p",
        default="FIFO",
        choices=["SRTN", "FIFO", "RR"],
        help="optional algorithm choice, SRTN, FIFO, or RR, default: FIFO")
    
    args = parser.parse_args()
    jobfile = args.jobfile
    p = args.p
    q = args.q

    readAssign(jobfile)
