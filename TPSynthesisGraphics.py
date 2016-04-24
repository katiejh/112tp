
def drawBoard(canvas, data, x, y):
    canvas.create_rectangle(x, y, x+data.boardDim, y+data.boardDim, fill="gray")

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

def drawScrollArrows(canvas, data):
    canvas.create_rectangle(data.margin, 
                            data.height-data.margin-data.scrollHeight,
                            data.margin+data.scrollWidth, 
                            data.height-data.margin, fill="gray")
    canvas.create_text(data.margin+data.scrollWidth//2, 
                            data.height-data.margin-data.scrollHeight//2,
                            text="Back")
    canvas.create_rectangle(data.width-data.margin-data.scrollWidth, 
                            data.height-data.margin-data.scrollHeight,
                            data.width-data.margin, 
                            data.height-data.margin, fill="gray")
    canvas.create_text(data.width-data.margin-data.scrollWidth//2, 
                            data.height-data.margin-data.scrollHeight//2,
                            text="Next")

def drawStepDots(canvas, data):
    totalWidth = data.pBoardX - (data.rBoardX+data.boardDim)
    space = totalWidth//data.numSteps
    for step in range(data.numSteps):
        cx,cy,r=space*(step+0.5)+data.boardDim+data.margin,5*data.boardDim//6,5
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="gray")

def drawReagentRect(canvas, data):
    totalWidth = data.pBoardX - (data.rBoardX+data.boardDim)
    x = data.margin*2 + data.boardDim
    y = data.subRY + data.margin
    canvas.create_rectangle(x, y, x+totalWidth-data.margin*2, y+50, fill="gray")

def drawButtons(canvas, data):
    for index in range(len(data.buttons)):
        # draws button
        canvas.create_rectangle(data.buttonX + index*data.scrollWidth, 
                                data.buttonY,
                                data.buttonX + (index+1)*data.scrollWidth, 
                                data.buttonY + data.scrollHeight, 
                                fill="gray")
        canvas.create_text(data.buttonX + (index+0.5)*data.scrollWidth, 
                                data.buttonY + data.scrollHeight//2,
                                text=data.buttons[index])     

def checkButtonClick(data, x, y):
    for index in range(len(data.buttons)):
        x1 = data.buttonX + index*data.scrollWidth
        y1 = data.buttonY
        x2 = data.buttonX + (index+1)*data.scrollWidth
        y2 = data.buttonY + data.scrollHeight
        if x1 <= x <= x2 and y1 <= y <= y2:
            data.button = data.buttons[index]

def moveStep(event, data):
    pass

from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    data.margin = 20 
    data.boardDim = data.width//3
    data.rBoardX, data.rBoardY = data.margin, data.margin
    data.pBoardX, data.pBoardY=data.width-data.margin-data.boardDim, data.margin
    data.subRX, data.subRY=data.margin, data.height-data.margin*4-data.boardDim
    data.subPX = data.width-data.margin-data.boardDim
    data.subPY = data.height-data.margin*4-data.boardDim
    data.scrollWidth, data.scrollHeight = 100, 40
    data.numSteps = 3
    data.buttons = ["Main Menu", "Submit", "Add Step", "Delete Step"]
    data.buttonX = data.margin*2 + data.boardDim//2 
    data.buttonY = data.subRY-data.margin-data.scrollHeight
    data.button = None

def mousePressed(event, data):
    checkButtonClick(data, event.x, event.y)
    if data.button == "Add Step":
        data.numSteps += 1
        data.button = None
    elif data.button == "Delete Step":
        data.numSteps -= 1
        data.button = None
    moveStep(event, data)

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    drawBoard(canvas, data, data.rBoardX, data.rBoardY)
    drawBoard(canvas, data, data.pBoardX, data.pBoardY)
    drawBoard(canvas, data, data.subRX, data.subRY)
    drawBoard(canvas, data, data.subPX, data.subPY)
    drawRxnArrow(canvas, data, data.rBoardY)
    drawRxnArrow(canvas, data, data.subPY)
    drawScrollArrows(canvas, data)
    drawStepDots(canvas, data)
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

run(700, 800)