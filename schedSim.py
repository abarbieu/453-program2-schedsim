import sys
import numpy as np
import argparse

def readAssign(file):
    f = open(file, mode='r')
    lines = np.array([l.strip('\n').split(' ') for l in f.readlines()], dtype=float)
    f.close()
    return lines[lines[:,1].argsort()]

def printTurnaround(jobs, wait):
    for i in range(len(jobs)):
        print(f"Job {i:3d} -- Turnaround {wait[i] + jobs[i,0]:3.2f} Wait {wait[i]:3.2f}")

def fifo(jobs):
    wait = [0]*jobs.shape[0]
    i = 0
    time = 0
    while i < len(jobs):
        time = max(time,jobs[i,1])
        wait[i] += time - jobs[i,1]
        time += jobs[i,0]
        i += 1
    return wait

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

    jobs = readAssign(jobfile)
    wait=fifo(jobs)

    printTurnaround(jobs,wait)
    
