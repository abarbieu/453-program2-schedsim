import numpy as np
import argparse

def readAssign(file):
    f = open(file, mode='r')
    lines = np.array([l.strip('\n').split(' ') for l in f.readlines()], dtype=float)
    f.close()
    return lines[lines[:,1].argsort()]

def printStats(jobs, endTs):
    turnSum=0
    waitSum=0
    for i in range(len(jobs)):
        turnaround = endTs[i] - jobs[i,1]
        wait = turnaround - jobs[i,0]
        turnSum+=turnaround
        waitSum+=wait
        print(f"Job {i:3d} -- Turnaround {turnaround:3.2f}  Wait {wait:3.2f}")
    print(f"Average -- Turnaround {turnSum/jobs.shape[0]:3.2f}  Wait {waitSum/jobs.shape[0]:3.2f}")

def fifo(jobs):
    endTs = [0]*jobs.shape[0]
    i = 0
    time = 0
    while i < len(jobs):
        time = max(time,jobs[i,1])
        time += jobs[i,0]
        endTs[i] = time
        i += 1
    return endTs

def srtn(alljobs):
    jobs = alljobs.copy()
    endTs=[0]*jobs.shape[0]
    i = 0
    currjob=i
    readyJobs = np.array([currjob])
    t=jobs[currjob,1] # t starts when job0 arrives
    iters=0

    while jobs[:,0].sum() > 0:
        iters+=1
        currjob = readyJobs[0]
        # if there are more jobs and the next job starts before this one ends
        if i < len(jobs)-1 and (jobs[i+1,1]-t) < jobs[currjob,0]:
            i += 1 # next starting job
            startI = jobs[i,1]
            # print(f"t: {t}, Next: {i}, t+={startI-t}, curr: {currjob}")
            jobs[currjob,0] -= startI-t # "run" this job until the next starts
            readyJobs = np.append(readyJobs, i)
            readyJobs = readyJobs[jobs[readyJobs,0].argsort()] # add job to ready jobs, sort by burst time
            # print(readyJobs,i)
            t += startI - t
        else:
            # print(f"t: {t}, Finish: {currjob} @t={t+jobs[currjob,0]}")
            readyJobs = readyJobs[1:] # pop job off queue
            t += jobs[currjob,0] # "run" job for remaining time
            endTs[currjob] = t
            jobs[currjob,0] = 0
    return endTs

def rr(alljobs, q):
    jobs = alljobs.copy()
    i=0
    t=0
    endTs = [0]*jobs.shape[0]

    while jobs[:,0].sum() > 0:
        if t < jobs[i,1]: # job hasn't started yet
            t = max(t,min(jobs[jobs[:,0] > 0][:,1])) # if no jobs are active, jump to when the next one starts
        elif jobs[i,0] > 0:
            timeran = min(q, jobs[i,0])
            # print(f"{i} ran for {timeran} from {t} to {t+timeran}")
            t+=timeran
            jobs[i,0]-=timeran
            if jobs[i,0] == 0:
                endTs[i] = t
        i = (i+1) % jobs.shape[0]
    return endTs
    



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
    q = float(args.q)

    jobs = readAssign(jobfile)
    endTs=None
    if p == "SRTN":
        endTs=srtn(jobs)
    elif p == "RR":
        endTs=rr(jobs, q)
    else:
        endTs=fifo(jobs)

    printStats(jobs,endTs)
    
