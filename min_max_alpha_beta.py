import math 
def minmax(currentDepth,IndexNode,maxturn,scores,targetdepth):
    if currentDepth==targetdepth:
        return scores[IndexNode]
    if maxturn:
        return max(minmax(currentDepth+1,IndexNode*2,False,scores,targetdepth),minmax(currentDepth+1,IndexNode*2+1,False,scores,targetdepth))
    else:
        return min(minmax(currentDepth+1,IndexNode*2,True,scores,targetdepth),minmax(currentDepth+1,IndexNode*2+1,True,scores,targetdepth))

scores=[2,4,3,6,7,8,1,0]
treedepth=math.log(len(scores),2)
print("Optimal score:",end="")
print(minmax(0,0,True,scores,treedepth))



