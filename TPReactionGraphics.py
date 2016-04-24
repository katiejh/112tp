from tkinter import *
import tkinter.simpledialog
import TermProject as TP

def drawBoard(canvas, data, x, y):
    canvas.create_rectangle(x, y, x+data.boardDim, y+data.boardDim, fill="gray")

def drawReactant(canvas, data, x, y):
    if data.reactant != None:
        data.reactant.drawMolecule(canvas, data.TPData, x, y, data.boardDim)

def drawProduct(canvas, data, x, y):
    if data.product != None:
        data.product.drawMolecule(canvas, data.TPData, x, y, data.boardDim)

def drawRxnArrow(canvas, data, y):
    canvas.create_line(data.rBoardX+data.boardDim+data.margin, 
                        data.boardDim//2 + y, 
                        data.pBoardX-data.margin, 
                        data.boardDim//2 + y, width=3)
    canvas.create_line(data.pBoardX-data.margin*2, data.boardDim//3 + y, 
                        data.pBoardX-data.margin, 
                        data.boardDim//2 + y, width=3)
    canvas.create_line(data.pBoardX-data.margin*2, data.boardDim//3*2 + y, 
                        data.pBoardX-data.margin, 
                        data.boardDim//2 + y, width=3)

def drawReagentRect(canvas, data):
    totalWidth = data.pBoardX - (data.rBoardX+data.boardDim)
    x = data.margin*2 + data.boardDim
    y = data.rBoardY + data.margin
    canvas.create_rectangle(x, y, x+totalWidth-data.margin*2, y+50, fill="gray")
    if data.reagent != None:
        canvas.create_text(x+(totalWidth-data.margin*2)//2, y+25, 
                            text=data.reagent)

def drawButtons(canvas, data):
    for index in range(len(data.buttons)):
        # draws button
        canvas.create_rectangle(data.buttonX + index*data.buttonWidth, 
                                data.buttonY,
                                data.buttonX + (index+1)*data.buttonWidth, 
                                data.buttonY + data.buttonHeight, 
                                fill="gray")
        canvas.create_text(data.buttonX + (index+0.5)*data.buttonWidth, 
                                data.buttonY + data.buttonHeight//2,
                                text=data.buttons[index])     

def checkButtonClick(data, x, y):
    for index in range(len(data.buttons)):
        x1 = data.buttonX + index*data.buttonWidth
        y1 = data.buttonY
        x2 = data.buttonX + (index+1)*data.buttonWidth
        y2 = data.buttonY + data.buttonHeight
        if x1 <= x <= x2 and y1 <= y <= y2:
            data.button = data.buttons[index]

def checkReactantBoxClick(data, x, y):
    x1 = data.rBoardX
    y1 = data.rBoardY
    x2 = x1+data.boardDim
    y2 = y1+data.boardDim
    if x1 <= x <= x2 and y1 <= y <= y2:
        data.mode = "Draw Atoms"
        TP.init(data.TPData)
        if data.reactant != None: data.TPData.atoms = data.reactant.atoms

def checkReagentBoxClick(data, x, y):
    totalWidth = data.pBoardX - (data.rBoardX+data.boardDim)
    x1 = data.margin*2 + data.boardDim
    y1 = data.rBoardY + data.margin
    x2 = x1+totalWidth-data.margin*2
    y2 = y1+50
    if x1 <= x <= x2 and y1 <= y <= y2:
        data.reagent = tkinter.simpledialog.askstring("Reagent", "Reagent:")


def moveStep(event, data):
    pass




####################################
# customize these functions
####################################

def init(data):
    class Struct(object): pass
    data.TPData = Struct()
    data.width = 700
    data.height = 800
    data.margin = 20 
    data.boardDim = data.width//3
    data.rBoardX, data.rBoardY = data.margin, data.width//4
    data.pBoardX, data.pBoardY=data.width-data.margin-data.boardDim, data.width//4
    data.buttons = ["Main Menu", "Submit"]
    data.buttonX = data.margin + data.boardDim
    data.buttonY = data.margin
    data.button = None
    data.buttonWidth, data.buttonHeight = 100, 40
    data.mode = "Reaction Practice"
    data.reactant = None 
    data.reagent = None
    data.product = None

def mousePressed(event, data):
    if data.mode == "Draw Atoms": 
        drawReturn = TP.mousePressed(event, data.TPData)
        if drawReturn == "Cancel": data.mode = "Reaction Practice"
        elif drawReturn == None: pass
        else: 
            data.reactant = drawReturn
            data.mode = "Reaction Practice"
    else:
        checkButtonClick(data, event.x, event.y)
        checkReactantBoxClick(data, event.x, event.y)
        checkReagentBoxClick(data, event.x, event.y)
        print(data.mode)
        if data.button == "Main Menu": return True
        elif data.button == "Submit":
            print(data.reactant)
            data.product = TP.substitutionRxn(data.reactant, data.reagent)
            if data.product == None:
                data.product = TP.eliminationRxn(data.reactant, data.reagent)
        else: return False

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    if data.mode == "Draw Atoms": TP.redrawAll(canvas, data.TPData)
    else:
        drawBoard(canvas, data, data.rBoardX, data.rBoardY)
        drawReactant(canvas, data, data.rBoardX, data.rBoardY)
        drawBoard(canvas, data, data.pBoardX, data.pBoardY)
        drawProduct(canvas, data, data.pBoardX, data.pBoardY)
        drawRxnArrow(canvas, data, data.rBoardY)
        drawReagentRect(canvas, data)
        drawButtons(canvas, data)

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

#run(700, 800)