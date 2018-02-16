import numpy as np
from bokeh.charts import Histogram, show

# Change For Different Sessions
        
fiveStarFocus = .03
fiveStar = .03
fourStar = .58
threeStar = 1-fiveStarFocus-fiveStar-fourStar

focusDict = {1:'b', 
             2:'g',
             3:'g',
             4:'w'
             }
wantFocus = [1,2]
sampleSize = 10000

fives = {"r":37,"b":28,"g":19,"w":20}
fours = {"r":29,"b":26,"g":18,"w":25}
threes =  {"r":15,"b":12,"g":9,"w":13}

# FUNCTIONS
def detRarity(n, pulled):
    if pulled>=120:                                                  # Max Pity
        r = np.random.random()
        if r>fiveStarFocus/(fiveStarFocus+fiveStar):
            return 6
        else: return 5
    pityplier = int(pulled/5)
    if n > ((1-fiveStarFocus) - (pityplier*fiveStarFocusPlus)):      
        return 6
    if n > ((1-fiveStarFocus - fiveStar) - pityplier*fiveStarPlus):
        return 5
    if n > ((1-fiveStarFocus - fiveStar - fourStar)):
        return 4
    else: 
        return 3
    
def detColorNonFocus(rarity):
    c = np.random.random()
    if rarity == 5:
        if c > 1-fivesProb['w']:
            return 'w'
        elif c > 1-fivesProb['r']-fivesProb['w']:
            return 'r'
        elif c > 1-fivesProb['b']-fivesProb['r']-fivesProb['w']:
            return 'b'
        else: 
            return 'g'
    elif rarity == 4:
        if c > 1-foursProb['w']:
            return 'w'
        elif c > 1-foursProb['w']-foursProb['r']:
            return 'r'
        elif c > 1-foursProb['w']-foursProb['r']-foursProb['b']:
            return 'b'
        else: 
            return 'g'
    else:
        if c > 1-threesProb['w']:
            return 'w'
        elif c > 1-threesProb['w']-threesProb['r']:
            return 'r'
        elif c > 1-threesProb['w']-threesProb['r']-threesProb['b']:
            return 'b'
        else: 
            return 'g'


def detColorFocus():
    r = np.random.random()
    for i in range(focusCount):
        if r > (1-((i+1)/focusCount)):
            return focusDict[int(i+1)]+str(int(i+1))
        
def orbsForPull(n):
    if n == 1:
        return 5
    if n == 5:
        return 3
    else:
        return 4



# Definitions 

fiveStarFocusPlus = .005*fiveStarFocus/(fiveStarFocus+fiveStar)
fiveStarPlus = .005-fiveStarFocusPlus
fourStarMinus = .005*fourStar/(fourStar+threeStar)
threeStarMinus = .005-fourStarMinus

focusCount = len(focusDict)

orbsUsed = []
totalOtherFiveStars = []

fivesProb = {}
foursProb = {}
threesProb = {}

rgb = ["r","b","w"]
for i in rgb:
    fivesProb[i] = fives[i]/sum(fives.values())
    foursProb[i] = fours[i]/sum(fours.values())
    threesProb[i] = threes[i]/sum(threes.values())

otherPulls = {'3':0,'4':0,'5':0,'6':0}
    

for sampleNumber in range(sampleSize):                                 # Sample of X pulls where i get ALL focus i want
    sampleStillWant = []                               # 
    pullColorStillNeed =  []
    for character in wantFocus:
        sampleStillWant.append(focusDict[character]+str(character))
        pullColorStillNeed.append(focusDict[character])
    gotAllRare = False
    orbCount = 0
    totalPulls = 0
    otherFives = 0
    while gotAllRare == False:                                  # decide whether or not to pull again
        pullList = []                                           # randomizing the pulls
        pullNumber = 0
        for i in range(5):
            r = np.random.random()
            pull = detRarity(r, totalPulls) 
            if pull==6:
                pullList.append(str(pull) + detColorFocus())
            else:
                pullList.append(str(pull) + detColorNonFocus(pull))
        for pull in pullList:                                        # For each individual in a set of 5
            if pull[1] in pullColorStillNeed:                        # if its still a color i need
                pullNumber = pullNumber + 1                          # I pull it from the set 
                totalPulls = totalPulls + 1
                orbCount = orbCount + orbsForPull(pullNumber)        # purchasing and adding to orbs
                if pull[1:] in sampleStillWant:                         # if the pull is a focus 
                    sampleStillWant.remove(pull[1:])                    # remove that 
                    pullColorStillNeed.remove(pull[1])
                if int(pull[0]) >= 5:
                    totalPulls = 0
                otherPulls[pull[0]] = otherPulls[pull[0]] + 1
                    

        if len(sampleStillWant) == 0:
            gotAllRare = True
            
            
            
            
    orbsUsed.append(orbCount)


    
print("Average orbs required for pulling", str(len(wantFocus)) + " focus heroes:", str(np.mean(orbsUsed)))
print("You got an average of:\n", otherPulls['3']/sampleSize,"3 stars\n",
      otherPulls['4']/sampleSize,"4 stars\n",
      otherPulls['5']/sampleSize,"5 stars\n",
      otherPulls['6']/sampleSize-len(wantFocus),"other focus characters")

print("for an average of", sum(otherPulls.values())/sampleSize, "new characters at a price of", round(sum(orbsUsed)/sum(otherPulls.values()),3),'orbs per character')
show(Histogram(orbsUsed, plot_width=1800, plot_height=900))
    
    
    
        
