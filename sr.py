import sys,logging
from BallotBox import BallotBox

logging.basicConfig(level=logging.DEBUG)

with open(sys.argv[1],"r") as ballots:
  B=BallotBox(ballots.readline().strip())
  for line in ballots:
    fields=line.strip().split(":")
    if len(fields)>=3: sys.exit("Malformed input")
    elif len(fields)==2: B.vote(fields[0].strip(),int(fields[1]))
    elif len(fields[0].strip())>0: B.vote(fields[0].strip())

print("Ballot box: "+str(B))
print("Sequential runoff winner: "+B.sequentialRunoff())

