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
    self.__candidates=candidates;
    self.__data={}
    
  def size(self):
    return len(self.__data)
    
  def numberOfCandidates(self):
    return len(self.__candidates)
    
  def rankings(self):
    return self.__data.keys()
    
  def vote(self,ranking,mult=1):
    c=Counter(ranking);
    mc=c.most_common(1);
    if mc[0][1]!=1: sys.exit("Invalid ballot: "+ranking+". Candidate "+mc[0][0]+" appears "+mc[0][1]+" times.")
    if not set(c).issubset(self.__candidates): sys.exit("Invalid ballot: "+ranking+". A candidate is not on the list ("+self.__candidates+")")  
    prev=self.__data.get(ranking,0)
    self.__data[ranking]=prev+mult
    
  def __str__(self):
    return self.__data.__str__()

  def countTop(self):
    result=dict.fromkeys(self.__candidates,0)
    for i in self.__data: result[i[0]]+=self.__data[i]
    logging.debug("CountTop returns with "+str(result))
    return result

  def pluralityWinner(self):
    result=sorted(self.countTop().items(), key=lambda c: c[1])
    return result[len(result)-1][0] #for now only one winner is returned, even in the case of a tie  
    
  def pluralityLoser(self):
    result=sorted(self.countTop().items(), key=lambda c: c[1])
    return result[0][0] #for now only one loser is returned, even in the case of a tie
    
  def removeLoser(self):
    """This function removes the candidate with the fewest number of top votes."""
    if not self.__candidates: raise Excpetion()
    loser=self.pluralityLoser()
    logging.debug("Removing "+loser)
    self.__candidates=self.__candidates.replace(loser,"")
    datacopy=self.__data; self.__data={}
    for i in datacopy:
      newranking=i.replace(loser,"")
      if (newranking): self.vote(newranking,datacopy[i])
    logging.debug("New candidate list: "+str(self.__candidates))
    logging.debug("New ballot box: "+str(self.__data))
      
  def sequentialRunoff(self,candidates=1):
    BB=self
    while BB.numberOfCandidates()>candidates:
      BB.removeLoser() #This does not remove a candidate with no top votes, but those candidates can not win anyway. However, we have to rething this approach for mutiple winners.
    return next(iter(BB.rankings()))[0]
