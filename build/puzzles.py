#
# Script to generate valid puzzles for Gods and Demons

options = ['god', 'knight', 'knave', 'demon']


pairs = []
for i in options:
    for j in options:
        pairs.append([i,j])
print(pairs)

#lets figure out all the way 'A' could be lying, and all the ways 'B' could be lying

mortals = ['knight','knave']
truthfuls =['god','knight']

aLying = []
bLying = []
for i in options:
    aLying.append(['demon',i])
    aLying.append(['knave',i])
    bLying.append([i,'demon'])
    bLying.append([i,'knave'])

#let's have a function that creates the sets of pairs based on two lists
def fromLists(a,b):
    res = []
    for i in a:
        for j in b:
            res.append([i,j])
    return res

    # return the list that is the intersection of two lists
def intersect(a, b):
    return [item for item in a if item in b]
    
# return the list that is the union of two lists
def union(a, b):
    return list(a) + [item for item in b if item not in a]

# return the list that is the complement of two lists (based on the big list of pairs)
def complement(a):
    return [item for item in pairs if item not in a]

# return list a - list b
def difference(a,b):
    return [item for item in a if item not in b]

    # now from mortals, we can define the immortals
immortals = difference(options,mortals)
liars = difference(options, truthfuls)

# we introduce the idea of 'sides' and of 'dimensions'
def sameSide(x):
    if (x == 'god' or x=='knight'):
        return truthfuls
    return liars

def sameDimension(x):
    if (x=='god' or x== 'demon'):
        return immortals
    return mortals

aTruthing = complement(aLying)
bTruthing = complement(bLying)

# aX(value) returns all pairs where 'A' is value
def aX(value):
    res = []
    for i in options:
        res.append([value, i])
    return res

#bX(value) returns all pairs where 'B' is value
def bX(value):
    res=[]
    for i in options:
        res.append([i,value])
    return res

# Let's have functions that create the states of affairs arising from A's statements, B's statements, 
# and then the solution must be in the intersection of the two.

def aPossible(aStatement):
    aTruths = intersect(aStatement, aTruthing)
    aLies = intersect(complement(aStatement),aLying)
    return union(aTruths, aLies)

def bPossible(bStatement): 
    bTruths = intersect(bStatement, bTruthing)
    bLies = intersect(complement(bStatement),bLying)
    return union(bTruths, bLies)

def solutions(aStatement, bStatement):
    return intersect(aPossible(aStatement),bPossible(bStatement))

def positiveStatement(option, sets, article = "a"):
    return {"statement":"I am "+ article + " "  + option, "type":option, "pairs": sets}
def negativeStatement(option, sets, article = "a"):
    return {"statement":"I am not " + article + " "+ option,"type": option, "pairs": sets}

aStatements = []
bStatements = []
for i in options:
    aStatements.append(positiveStatement(i,aX(i)))
    aStatements.append(negativeStatement(i,complement(aX(i))))
    bStatements.append(positiveStatement(i,bX(i)))
    bStatements.append(negativeStatement(i,complement(bX(i))))

def runAllStatements():
    counter = 1
    for a in aStatements:
        for b in bStatements:
            s = solutions(a["pairs"], b["pairs"])
            if (len(s) == 1):
                print("puzzle: " + str(counter))
                counter = counter + 1
                print("A says: " + a["statement"] + ", B says: " + b["statement"])
                print("The solution is that A is a "+ s[0][0] + " and B is a " + s[0][1])
                print("----------------------------------------------------------")

def otherStatement(option, sets):
    return {"statement":"They are a " + option, "type":option, "pairs": sets}

def otherNotStatement(option, sets):
    return {"statement":"They are not a " + option, "type":option, "pairs": sets}

for i in options:
    aStatements.append(otherStatement(i,bX(i)))
    aStatements.append(otherNotStatement(i,complement(bX(i))))
    bStatements.append(otherStatement(i,aX(i)))
    bStatements.append(otherNotStatement(i,complement(aX(i))))

def sideStatement(side,sets ):
        return {"statement":"I am " + side, "type":side, "pairs": sets}
def weAreBoth(option,sets):
    return {"statement":"We are both " + option, "type":option, "pairs": sets}

def iAmTheyAre(option1, option2, sets):
    return {"statement":"I am a  " + option1 + " and they are a " + option2, "type":option1, "pairs": sets}

aStatements.append(sideStatement("immortal", fromLists(immortals, options)))
aStatements.append(sideStatement("mortal", fromLists(mortals, options)))
aStatements.append(sideStatement("truth-teller", fromLists(truthfuls, options)))
aStatements.append(sideStatement("liar", fromLists(liars, options)))

bStatements.append(sideStatement("immortal", fromLists(options, immortals)))
bStatements.append(sideStatement("mortal", fromLists(options, mortals)))
bStatements.append(sideStatement("truth-teller", fromLists(options, truthfuls)))
bStatements.append(sideStatement("liar", fromLists(options, liars)))

for i in options:
    aStatements.append(weAreBoth(i + "s", [[i,i]]))
    bStatements.append(weAreBoth(i + "s", [[i,i]]))

aStatements.append(weAreBoth("liars",fromLists(liars,liars)))
bStatements.append(weAreBoth("liars",fromLists(liars,liars)))

aStatements.append(weAreBoth("truthful",fromLists(truthfuls,truthfuls)))
bStatements.append(weAreBoth("truthful",fromLists(truthfuls,truthfuls)))

aStatements.append(weAreBoth("immortal",fromLists(immortals,immortals)))
bStatements.append(weAreBoth("immortal",fromLists(immortals,immortals)))

aStatements.append(weAreBoth("mortals",fromLists(mortals,mortals)))
bStatements.append(weAreBoth("mortals",fromLists(mortals,mortals)))

aStatements.append(iAmTheyAre("mortal","immortal", fromLists(mortals,immortals)))
bStatements.append(iAmTheyAre("mortal","immortal", fromLists(immortals,mortals)))

aStatements.append(iAmTheyAre("liar","truth-teller", fromLists(liars,truthfuls)))
bStatements.append(iAmTheyAre("liar","truth-teller", fromLists(truthfuls,liars)))

for i in options:
    for j in options:        
        aStatements.append(iAmTheyAre(i,j,[[i,j]]))
        bStatements.append(iAmTheyAre(i,j,[[j,i]]))

bothImmortal = fromLists(immortals,immortals)

bothMortal = fromLists(mortals, mortals)
fromSameDimension = union(bothImmortal, bothMortal)

dimensionStatement = {"statement":"We are from the same dimension", "type":"dimension", "pairs": fromSameDimension}
aStatements.append(dimensionStatement)
bStatements.append(dimensionStatement)

differentDimensions = difference(pairs, fromSameDimension)

diffDimensionStatement = {"statement":"We are from a different dimension", "type":"dimension", "pairs": differentDimensions}
aStatements.append(diffDimensionStatement)
bStatements.append(diffDimensionStatement)

def iAmORTheyAre(option1, option2, sets):
    return {"statement":"I am a  " + option1 + " or they are a " + option2, "type":option1, "pairs": sets}

for i in options:
    for j in options:        
        aStatements.append(iAmORTheyAre(i,j, union(aX(i),bX(j))))
        bStatements.append(iAmORTheyAre(i,j, union(aX(j),bX(i))))

for i in options:
    aStatements.append(iAmTheyAre(i, "mortal", fromLists([i],mortals)))
    aStatements.append(iAmORTheyAre(i,"mortal", union(aX(i),fromLists(options,mortals))))
    aStatements.append(iAmTheyAre(i, "immortal", fromLists([i],immortals)))
    aStatements.append(iAmORTheyAre(i,"immortal", union(aX(i),fromLists(options,immortals))))
    ##
    bStatements.append(iAmTheyAre(i, "mortal", fromLists(mortals,[i])))
    bStatements.append(iAmORTheyAre(i,"mortal", union(bX(i),fromLists(options,mortals))))
    bStatements.append(iAmTheyAre(i, "immortal", fromLists(immortals,[i])))
    bStatements.append(iAmORTheyAre(i,"immortal", union(bX(i),fromLists(options,immortals))))

    
sameType = []
for i in options:
    sameType.append([i,i])
sameTypeStatement ={"statement":"We are the same type", "type":"same", "pairs":sameType }
aStatements.append(sameTypeStatement)
bStatements.append(sameTypeStatement)

runAllStatements()
  









