import math

class Atom(object):
    def __init__(self, element, x, y):
        self.element = element #what element i.e C,N,O
        self.x = x
        self.y = y
        self.bonds = None
        self.radius = 15
        self.scaleX = None
        self.scaleY = None

    # sets max bonds depending on element
    def getMaxBonds(self):
        if self.element == "C": return 4
        elif self.element == "N": return 3
        elif self.element == "O" or self.element == "Mg": return 2
        elif self.element == "H" or self.element == "Br": return 1
        #add more elements as needed

    # returns current number of bonds a given atom has
    def getNumBonds(self):
        numBonds = 0
        for key in self.bonds:
            numBonds += self.bonds[key]
        print(self, numBonds)
        return numBonds

    # returns the atoms that are bound to an atom
    def getBoundAtoms(self):
        result = []
        if self.bonds == None: self.bonds = dict()
        for key in self.bonds:
            result += [key]
        return result

    # returns the specific atoms of a certain element bound to an atom
    # double bonds first, single bonds second
    def getSpecificBoundAtoms(self, element):
        result = []
        if self.bonds == None: self.bonds = dict()
        for key in self.bonds:
            if key.element == element and self.bonds[key] == 2:
                result = [key] + result
            elif key.element == element and self.bonds[key] ==1:
                result += [key]
        return result  


    # adds to dictionary of bonds {atom: bond order}
    def bond(self, other):
        if self.bonds == None: self.bonds = dict()
        if other.bonds == None: other.bonds = dict()
        if self.getNumBonds()<self.getMaxBonds():
            if other.getNumBonds()<other.getMaxBonds():
                # creates first bond
                if self not in other.bonds and other not in self.bonds:
                    other.bonds[self] = 1
                    self.bonds[other] = 1
                # increases bond order (i.e. single to double bond)
                else:
                    self.bonds[other] += 1
                    other.bonds[self] += 1

    def unbond(self, other):
        if self not in other.bonds or other not in self.bonds:
            return None
        elif self.bonds[other] > 1 or other.bonds[self] > 1:
            self.bonds[other] -= 1
            other.bonds[self] -= 1
        elif self.bonds[other] <= 1 or other.bonds[self] <= 1:
            self.bonds.pop(other)
            other.bonds.pop(self)

    def move(self, newX, newY):
        self.x = newX
        self.y = newY

    def deleteAllBonds(self):
        if self.bonds != None:
            for other in self.bonds:
                other.bonds.pop(self)

    # draws the atoms
    def drawAtoms(self, canvas):
        (cx, cy, r) = (self.x, self.y, self.radius)  
        # draws the atom itself
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="white")
        canvas.create_text(cx, cy, text=self.element)

    # draws the bonds in between atoms
    def drawBonds(self, canvas, data):
        if self.bonds != None:
            for other in self.bonds:
                #draws the middle or single line
                if self.bonds[other] == 1 or self.bonds[other] == 3:
                    canvas.create_line(self.x, self.y, other.x, other.y)
                #draws the 2 edge lines
                if self.bonds[other] == 2 or self.bonds[other] == 3:
                    # finds the change in x and y to move the lines
                    # away from the original center line
                    r = self.radius/2
                    #checks for vertical case(dont want to divide by zero later)
                    if other.x-self.x == 0:
                        canvas.create_line(self.x+r,self.y,other.x+r,other.y)       
                        canvas.create_line(self.x-r,self.y,other.x-r,other.y)
                    #checks for horizontal case
                    elif other.y-self.y == 0:
                        canvas.create_line(self.x,self.y-r,other.x,other.y-r)                               
                        canvas.create_line(self.x,self.y+r,other.x,other.y+r) 
                    else:
                        slope = (other.y-self.y)/(other.x-self.x)
                        pslope = -1*(1/slope)
                        theta = math.atan(pslope)
                        dx, dy = r*math.cos(theta), r*math.sin(theta)  
                        # draws the normal double bond 
                        # (or two edges of triple bond)     
                        canvas.create_line(self.x+dx,self.y+dy,
                                        other.x+dx,other.y+dy)          
                        canvas.create_line(self.x-dx,self.y-dy,
                                        other.x-dx,other.y-dy)

    def drawScaleBonds(self, canvas, data):
        if self.bonds != None:
            for other in self.bonds:
                newX, newY = self.scaleX, self.scaleY
                newOX, newOY = other.scaleX, other.scaleY
                #draws the middle or single line
                if self.bonds[other] == 1 or self.bonds[other] == 3:
                    canvas.create_line(newX, newY, newOX, newOY)
                #draws the 2 edge lines
                if self.bonds[other] == 2 or self.bonds[other] == 3:
                    # finds the change in x and y to move the lines
                    # away from the original center line
                    r = self.radius/2
                    #checks for vertical case(dont want to divide by zero later)
                    if other.x-self.x == 0:
                        canvas.create_line(newX+r,newX,newOX+r,newOY)       
                        canvas.create_line(newX-r,newY,newOX-r,newOY)
                    #checks for horizontal case
                    elif other.y-self.y == 0:
                        canvas.create_line(newX,newY-r,other.x,other.y-r)                               
                        canvas.create_line(newX,newY+r,newOX,newOY+r) 
                    else:
                        slope = (newOY-newY)/(newOX-newX)
                        pslope = -1*(1/slope)
                        theta = math.atan(pslope)
                        dx, dy = r*math.cos(theta), r*math.sin(theta)  
                        # draws the normal double bond 
                        # (or two edges of triple bond)     
                        canvas.create_line(newX+dx,newY+dy,
                                        newOX+dx,newOY+dy)          
                        canvas.create_line(newX-dx,newY-dy,
                                        newOX-dx,newOY-dy)

    def drawScaleAtoms(self, canvas):
        (cx, cy, r) = (self.scaleX, self.scaleY, self.radius)  
        # draws the atom itself
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="white")
        canvas.create_text(cx, cy, text=self.element)

    # checks to see if clicked in a placed atom
    def atomClicked(self, x, y):
        distance = ((self.x-x)**2+(self.y-y)**2)**0.5
        if distance <= self.radius:
            return True
        else: return False

class Molecule(object):
    def __init__(self, atoms):
        self.atoms = atoms
        self.funcGroup = findFuncGroup(self.atoms)

    def drawMolecule(self, canvas, data, x1, y1, dim):
        for atom in self.atoms:
            atom.scaleX = (atom.x-100)*dim/data.boardDim+x1
            atom.scaleY = (atom.y-20)*dim/data.boardDim+y1
        for atom in self.atoms:
            atom.drawScaleBonds(canvas, data)
        for atom in self.atoms:
            atom.drawScaleAtoms(canvas)

from tkinter import *
import copy
import random

####################################
# customize these functions
####################################

def cleanUpAtoms(event, data):
    anchor = random.choice(data.atoms)
    seenAtoms = [anchor]
    for atom in anchor.getBoundAtoms():
        scaleBond(anchor, atom, seenAtoms, data)

def scaleBond(anchor, currentAtom, seenAtoms, data):
    if currentAtom not in seenAtoms:
        dx, dy = currentAtom.x - anchor.x, currentAtom.y - anchor.y
        scale = data.bondLength/(((dx**2)+(dy**2))**0.5)
        currentAtom.x = anchor.x + dx*scale
        currentAtom.y = anchor.y + dy*scale
        seenAtoms += [currentAtom]
        for nextAtom in currentAtom.getBoundAtoms():
            scaleBond(currentAtom, nextAtom, seenAtoms, data)

def substitutionRxn(molecule, reagent):
    print(molecule.funcGroup)
    print(molecule)
    if "Halide" not in molecule.funcGroup: return None
    else:
        if reagent == "H2O" or reagent == "NaOH":
            productAtoms = molecule.atoms   
            print("productAtoms", productAtoms)
            print("molecule.atoms", molecule.atoms) 
            halidesList = molecule.funcGroup["Halide"]
            molecule.atoms = copy.deepcopy(molecule.atoms)
            for pair in halidesList:
                carbon = pair[0]
                bromine = pair[1]

                print("halidesList", halidesList)
                print("bromine", bromine)
                for pAtom in productAtoms:
                    if pAtom.element == "Br":
                        productAtoms.remove(pAtom)
                oxygen = Atom("O", bromine.x, bromine.y)
                hydrogen = Atom("H", bromine.x+50, bromine.y+50)
                carbon.unbond(bromine)
                carbon.bond(oxygen)
                oxygen.bond(hydrogen)
                productAtoms += [oxygen, hydrogen]
                print("PRODFINAL", productAtoms)
            return Molecule(productAtoms)

def eliminationRxn(molecule, reagent):
    if "Halide" not in molecule.funcGroup: return None
    if reagent == "tBuONa":
        halidesList = molecule.funcGroup["Halide"]
        for pair in halidesList:
            carbon, bromine = pair[0], pair[1]
            boundToACarbon = carbon.getBoundAtoms()
            numC, numH = countBoundAtomTypes(boundToACarbon)
            if numC < 1: return None
            productAtoms = molecule.atoms
            molecule.atoms = copy.deepcopy(molecule.atoms)
            if numC >= 1:
                for atom in boundToACarbon:
                    if atom.element == "C":
                        boundToBCarbon = atom.getBoundAtoms()
                        numC, numH = countBoundAtomTypes(boundToBCarbon)
                        if numH >= 1:
                            for hydrogen in boundToBCarbon:
                                if hydrogen.element == "H":
                                    productAtoms.remove(bromine)
                                    productAtoms.remove(hydrogen)
                                    atom.unbond(hydrogen)
                                    carbon.unbond(bromine)
                                    carbon.bond(atom)
                                    return Molecule(productAtoms)


# turns atoms into molecule once hit submit
def findFuncGroup(atoms):
    funcGroup = dict()
    oxyList = []
    # adds amine, halide, grignard to dict if needed and makes oxyList
    funcGroup, oxyList = miscFindFuncGroupHelper(atoms, funcGroup, oxyList)
    # loops through the list of all the oxygens
    for oxygen in oxyList:
        # gets all the atoms bound to the oxygen
        boundAtoms = oxygen.getBoundAtoms()
        # counts the number of different types of atoms around the oxygen
        numC, numH = countBoundAtomTypes(boundAtoms)
        # if the oxygen is surrounded by 2 carbons: ether or ester
        if numC == 2:
            funcGroup, oxyList = caseCCHelper(boundAtoms, funcGroup,
                                              oxygen, oxyList)
        # if oxygen surrounded by 1C, 1H: alcohol or carb acid
        elif numC == 1 and numH == 1:
            funcGroup, oxyList = caseCHHelper(boundAtoms, funcGroup,
                                              oxygen, oxyList)
        # skips if a double bonded O to C.
        elif numC == 1 and numH == 0: continue
    # if none of the other types and still an oxygen left to assign: carbonyl
    for leftoverOxygen in oxyList:
        if "Carbonyl" not in funcGroup:
            toAppend = leftoverOxygen.getBoundAtoms() + [leftoverOxygen]
            funcGroup["Carbonyl"]=[toAppend]
        else: funcGroup["Carbonyl"].append(toAppend)
    return funcGroup

def miscFindFuncGroupHelper(atoms, funcGroup, oxyList):
    # goes through all the atoms
    for atom in atoms:
        if atom.element == "N":
            # amine: [Nitrogen]
            if "Amine" not in funcGroup: funcGroup["Amine"] = [[atom]]
            else: funcGroup["Amine"].append([atom])
        elif atom.element == "Br":
            boundAtoms = atom.getBoundAtoms()
            boundAtom = boundAtoms[0]
            if boundAtom.element == "Mg":
                carbon = boundAtom.getSpecificBoundAtoms("C")
                if "Grignard" not in funcGroup: 
                    # Grignard: [C, Mg, Br]
                    funcGroup["Grignard"] = [carbon + [boundAtom] + [atom]]
                else: 
                    funcGroup["Grignard"].append(carbon + [boundAtom] + [atom])
            else:
                carbon = atom.getSpecificBoundAtoms("C")
                if "Halide" not in funcGroup: 
                    # Halide: [cardon, halogen]
                    funcGroup["Halide"] = [carbon + [atom]]
                else: funcGroup["Halide"].append(carbon + [atom])
        # makes oxygen list to deal with oxygens later
        elif atom.element == "O": oxyList += [atom]  
    return funcGroup, oxyList

# counts the types of atoms around an oxygen
def countBoundAtomTypes(boundAtoms):
    numC, numH = 0, 0
    for boundAtom in boundAtoms:
        if boundAtom.element == "C":
            numC += 1
        elif boundAtom.element == "H":
            numH += 1
    return numC, numH

def caseCCHelper(boundAtoms, funcGroup, oxygen, oxyList):
    #loops through the 2 carbons bound to the oxygen
    for boundAtom in boundAtoms:
        # at a given carbon, looks at ITS neighbors
        carbonNeighbors = boundAtom.getBoundAtoms()
        numONeighbors = 0
        # checks to see how many oxygens the given carbon is bound to
        for carbonNeighbor in carbonNeighbors:
            if carbonNeighbor.element == "O": 
                numONeighbors += 1
        # if the carbon is bound to 2+ oxygens, we know it is an ester
        if numONeighbors > 1:
            # Ester: [carbon, double bond oxygen, single bond oxygen]
            if "Ester" not in funcGroup:
                oxygens = boundAtom.getSpecificBoundAtoms("O")
                funcGroup["Ester"]=[[boundAtom] + oxygens]
            else: funcGroup["Ester"].append([boundAtom] + oxygens)
            # removes oxygens from oxyList
            for oxygenToRemove in oxygens: oxyList.remove(oxygenToRemove)
    if numONeighbors == 1:
        toAppend = oxygen.getSpecificBoundAtoms("C") + [oxygen]
        # Ether: [carbon, carbon, oxygen]
        if "Ether" not in funcGroup: funcGroup["Ether"]=[toAppend]
        else: funcGroup["Ether"].append(toAppend)
        oxyList.remove(oxygen)
    return funcGroup, oxyList

def caseCHHelper(boundAtoms, funcGroup, oxygen, oxyList):
    #finds the carbon in the list
    for boundAtom in boundAtoms:
        if boundAtom.element == "C":
            # finds the atoms bound to this carbon
            carbonNeighbors = boundAtom.getBoundAtoms()
            numONeighbors = 0
            # looks for how many oxygens are bound to the carbon
            print("CNEIGHS", carbonNeighbors)
            for carbonNeighbor in carbonNeighbors:
                if carbonNeighbor.element == "O": 
                    numONeighbors += 1
            # if 2+ carbons: carboxylic acid
            print("NUMNEIGHBORS", numONeighbors)
            if numONeighbors > 1:
                if "CarbAcid" not in funcGroup:
                    oxygens = boundAtom.getSpecificBoundAtoms("O")
                    # CarbAcid: [carbon, oxygen, oxygen]
                    funcGroup["CarbAcid"]=[[boundAtom] + oxygens]
                else: funcGroup["CarbAcid"].append([boundAtom] + oxygens)
                print("oxyList", oxyList)
                for oxygenToRemove in oxygens: oxyList.remove(oxygenToRemove)
    # only 1 oxygen: alcohol
    if numONeighbors == 1:
        toAppend = oxygen.getSpecificBoundAtoms("C") + [oxygen]
        # Alcohol: [carbon, oxygen]
        if "Alcohol" not in funcGroup: funcGroup["Alcohol"]=[toAppend]
        else: funcGroup["Alcohol"].append(toAppend)
        oxyList.remove(oxygen)
    return funcGroup, oxyList

#loops through the possible element buttons to see if clicked
def checkElementClick(data, x, y):
    for index in range(len(data.elements)):
        x1 = data.margin
        y1 = data.margin + index*data.buttonDim
        x2 = data.margin + data.buttonDim
        y2 = data.margin + (index+1)*data.buttonDim
        if x1 <= x <= x2 and y1 <= y <= y2:
            data.atomToAdd = data.elements[index]

def checkModeClick(data, x, y):
    for index in range(len(data.modes)):
        x1 = data.modeX + index*data.modeWidth
        y1 = data.modeY
        x2 = data.modeX + (index+1)*data.modeWidth
        y2 = data.modeY + data.modeHeight
        if x1 <= x <= x2 and y1 <= y <= y2:
            data.mode = data.modes[index]
            data.atomToAdd = None
            data.atomToBond = None
            data.atomToMove = None
            data.atomToRemoveBond = None
            data.atomToHighlight = None

def checkGeneralButtonClick(data, x, y):
    for index in range(len(data.generals)):
        x1 = data.generalX + index*data.modeWidth
        y1 = data.generalY
        x2 = data.generalX + (index+1)*data.modeWidth
        y2 = data.generalY + data.modeHeight
        if x1 <= x <= x2 and y1 <= y <= y2:
            data.general = data.generals[index]

#checks to see if legal place to put element
def checkLegalAtomPlacement(data, x, y):
    for atom in data.atoms:
        if atom.atomClicked(x,y): return False
    x2 = data.boardX+data.boardDim
    y2 = data.boardY+data.boardDim
    if data.boardX <= x <= x2 and data.boardY <= y <= y2:
        return True
    else: return False

def drawBoard(canvas, data):
    canvas.create_rectangle(data.boardX, data.boardY, 
                            data.boardX+data.boardDim, 
                            data.boardY+data.boardDim, fill="gray")

def drawElementButtons(canvas, data):
    for index in range(len(data.elements)):
        #if clicked, highlights button
        if data.elements[index] == data.atomToAdd:
            color = "light yellow"
        else: color = "gray"
        # draws button
        canvas.create_rectangle(data.margin, data.margin + index*data.buttonDim,
                                data.margin + data.buttonDim, 
                                data.margin + (index+1)*data.buttonDim, 
                                fill=color)
        canvas.create_text(data.margin + data.buttonDim//2, 
                                data.margin + (index+0.5)*data.buttonDim,
                                text=data.elements[index])

def drawModeButtons(canvas, data):
    for index in range(len(data.modes)):
        #if clicked, highlights button
        if data.modes[index] == data.mode:
            color = "light yellow"
        else: color = "gray"
        # draws button
        canvas.create_rectangle(data.modeX + index*data.modeWidth, data.modeY,
                                data.modeX + (index+1)*data.modeWidth, 
                                data.modeY + data.modeHeight, 
                                fill=color)
        canvas.create_text(data.modeX + (index+0.5)*data.modeWidth, 
                                data.modeY + data.modeHeight//2,
                                text=data.modes[index])

def drawModeInstr(canvas, data):
    instr = ["Click an element to add. Click atoms sequentially to bond.", 
             "Click an atom and then the new location to move.",
             "Click an atom to remove.", 
             "Click atoms sequentially to decrease bond order."]
    for index in range(len(data.modes)):
        if data.modes[index] == data.mode:
            text = instr[index]
            canvas.create_text(data.generalX + 2*data.modeWidth, 
                                data.generalY + data.modeHeight*2,
                                text=text)

def drawGeneralButtons(canvas, data):
    for index in range(len(data.generals)):
        # draws button
        canvas.create_rectangle(data.generalX + index*data.modeWidth, 
                                data.generalY,
                                data.generalX + (index+1)*data.modeWidth, 
                                data.generalY + data.modeHeight, 
                                fill="gray")
        canvas.create_text(data.generalX + (index+0.5)*data.modeWidth, 
                                data.generalY + data.modeHeight//2,
                                text=data.generals[index])    

def addAtomsHelper(event, data):
    #if 1st click is occuring
    if data.atomToBond == None and data.atomToAdd == None:
        #checks to see if clicking inside existing atom 
        for atom in data.atoms:
            if atom.atomClicked(event.x, event.y) == True:
                data.atomToBond = atom
                data.atomToHighlight = atom 
        #checks to see if need to add an element 
        checkElementClick(data, event.x, event.y)
    #if 2nd click is occuring, and need to bond atoms
    elif data.atomToBond != None:
        for atom in data.atoms:
            if atom.atomClicked(event.x, event.y) == True:
                if atom != data.atomToBond:
                    atom.bond(data.atomToBond)
        data.atomToBond = None
        data.atomToHighlight = None
    # if 2nd click is occuring, and need to add atoms
    elif data.atomToAdd != None:
        if checkLegalAtomPlacement(data, event.x, event.y) == True:
            data.atoms.append(Atom(data.atomToAdd, event.x, event.y))
        data.atomToAdd = None

def moveAtomsHelper(event, data):
    if data.atomToMove == None:
        for atom in data.atoms:
            if atom.atomClicked(event.x, event.y) == True:
                data.atomToMove = atom
                data.atomToHighlight = atom
    elif data.atomToMove != None:
        if checkLegalAtomPlacement(data, event.x, event.y) == True:
            data.atomToMove.move(event.x, event.y)
            data.atomToMove = None
        data.atomToHighlight = None

def removeAtomsHelper(event, data):
        for atom in data.atoms:
            if atom.atomClicked(event.x, event.y) == True:
                atom.deleteAllBonds()
                data.atoms.remove(atom)

def removeBondsHelper(event, data):
    if data.atomToRemoveBond == None:
        for atom in data.atoms:
            if atom.atomClicked(event.x, event.y) == True:
                data.atomToRemoveBond = atom
                data.atomToHighlight = atom 
    elif data.atomToRemoveBond != None:
        for atom in data.atoms:
            if atom.atomClicked(event.x, event.y) == True:
                atom.unbond(data.atomToRemoveBond)
        data.atomToRemoveBond = None
        data.atomToHighlight = None

def init(data):
    data.atomToHighlight = None
    data.atoms = []
    data.molecules = []
    data.atomToBond = None
    data.atomToAdd = None
    data.margin = 20
    data.buttonDim = 50
    # possible elements to add
    data.elements = ["H", "C", "N", "O", "Br", "Mg"]
    # starting corner of board
    data.boardX, data.boardY = 100, 20
    data.boardDim = 500
    data.modes = ["Add", "Move", "Remove Atoms", "Remove Bonds"]
    data.modeX, data.modeY = 150, 550
    data.modeHeight, data.modeWidth = 50, 100
    data.mode, data.atomToMove, data.atomToRemoveBond = "Add", None, None
    data.generals = ["Clean Up", "Clear", "Cancel", "Submit"]
    data.generalX, data.generalY = data.modeX, 610
    data.general = None
    data.bondLength = 60

# structure of this function taken from hw8a
def mousePressed(event, data):
    checkModeClick(data, event.x, event.y)
    checkGeneralButtonClick(data, event.x, event.y)
    if data.mode == "Add":
        addAtomsHelper(event, data)
    elif data.mode == "Move":
        moveAtomsHelper(event, data)
    elif data.mode == "Remove Atoms":
        removeAtomsHelper(event, data)
    elif data.mode == "Remove Bonds":
        removeBondsHelper(event, data)
    if data.general == "Clear":
        init(data)
    elif data.general == "Clean Up":
        cleanUpAtoms(event, data)
    elif data.general == "Submit":
        return Molecule(data.atoms)
    elif data.general == "Cancel":
        return "Cancel"
    else: return None


def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    drawBoard(canvas, data)
    drawElementButtons(canvas, data)
    drawModeButtons(canvas, data)
    drawModeInstr(canvas, data)
    drawGeneralButtons(canvas, data)
    #draws bonds first so underneath atoms
    for atom in data.atoms:
        atom.drawBonds(canvas, data)
    for atom in data.atoms:
        # this draws the highlight if the atom is selected
        if atom == data.atomToHighlight:
            (cx, cy, r) = (atom.x, atom.y, atom.radius)  
            canvas.create_oval(cx-2*r, cy-2*r, 
                                cx+2*r, cy+2*r,fill="light yellow")
        atom.drawAtoms(canvas)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

# run(700, 800)