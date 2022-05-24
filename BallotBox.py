import logging,sys
from collections import Counter

#Work to do:
#- Multiple return values for pluraityWinner().
#- Multiple return values for pluralityLoser().
#- Implement tie breakers for sequentialRunoff().
#- Implement other voting methods.
#- Potentially implement a higher order class for actual names/ids for candidates.

class BallotBox:

  def __init__(self,candidates):
    mc=Counter(candidates).most_common(1)
    if mc[0][1]!=1: raise Exception("Invalid list of candidates: "+candidates+". Candidate "+mc[0][0]+" appears "+str(mc[0][1])+" times.")
    self.__candidates=candidates;
    self.__data={}
    
  def __str__(self):
    return self.__candidates+"; "+self.__data.__str__()

  def size(self):
    return len(self.__data)
    
  def numberOfCandidates(self):
    return len(self.__candidates)
    
  def rankings(self):
    return self.__data.keys()
    
  def vote(self,ranking,mult=1):
    #logging.debug("Voting: "+ranking+" x "+str(mult))
    c=Counter(ranking);
    mc=c.most_common(1);
    if mc[0][1]!=1: raise Exception("Invalid ballot: "+ranking+". Candidate "+mc[0][0]+" appears "+str(mc[0][1])+" times.")
    if not set(c).issubset(self.__candidates): raise Exception("Invalid ballot: "+ranking+". A candidate is not on the list ("+self.__candidates+")")  
    prev=self.__data.get(ranking,0)
    self.__data[ranking]=prev+mult
    
  def countTop(self):
    result=dict.fromkeys(self.__candidates,0)
    for i in self.__data: result[i[0]]+=self.__data[i]
    logging.debug("countTop() returns with "+str(result))
    return result

  def pluralityWinner(self):
    result=sorted(self.countTop().items(), key=lambda c: c[1])
    return result[len(result)-1][0] #for now only one winner is returned, even in the case of a tie  
    
  def pluralityLoser(self):
    result=sorted(self.countTop().items(), key=lambda c: c[1])
    return result[0][0] #for now only one loser is returned, even in the case of a tie
    
  def removeLoser(self):
    """This function removes the candidate with the fewest number of top votes."""
    if not self.__candidates: raise Excpetion("Candidate list is empty")
    loser=self.pluralityLoser()
    logging.debug("Removing "+loser)
    self.__candidates=self.__candidates.replace(loser,"")
    datacopy=self.__data; self.__data={}
    for i in datacopy:
      newranking=i.replace(loser,"")
      if (newranking): self.vote(newranking,datacopy[i])
    logging.debug("New ballot box: "+str(self))
      
  def sequentialRunoff(self,candidates=1):
    BB=self
    while BB.numberOfCandidates()>candidates:
      BB.removeLoser() #This does not remove a candidate with no top votes, but those candidates can not win anyway. However, we have to rething this approach for mutiple winners.
    return next(iter(BB.rankings()))[0]
