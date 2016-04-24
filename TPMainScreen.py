def drawMMButtons(canvas, data):
    for index in range(len(data.buttons)):
        canvas.create_rectangle(data.buttonX, data.buttonY + index*data.buttonHeight,
                                data.buttonX + data.buttonWidth, 
                                data.buttonY + (index+1)*data.buttonHeight, 
                                fill="gray")
        canvas.create_text(data.buttonX + data.buttonWidth//2, 
                                data.buttonY + (index+0.5)*data.buttonHeight,
                                text=data.buttons[index])

def checkButtonClick(data, x, y):
    for index in range(len(data.buttons)):
        x1 = data.buttonX 
        y1 = data.buttonY + index*data.buttonHeight
        x2 = data.buttonX + data.buttonWidth 
        y2 = data.buttonY + (index+1)*data.buttonHeight
        if x1 <= x <= x2 and y1 <= y <= y2:
            data.button = data.buttons[index]

from tkinter import *
import TPReactionGraphics as Rxn

####################################
# customize these functions
####################################

def init(data):
    data.margin = 20
    data.buttons = ["Synthesis Solver", "Synthesis Practice", 
                    "Reaction Practice"]
    data.buttonWidth, data.buttonHeight = 150, 40
    data.buttonX = data.width//2-data.buttonWidth//2
    data.buttonY = data.height//4
    data.button = None
    data.mode = "Main Menu"

def mousePressed(event, data):
    if data.mode == "Reaction Practice": 
        if Rxn.mousePressed(event, data.RxnData): data.mode = "Main Menu"
    else:
        checkButtonClick(data, event.x, event.y)
        data.mode = data.button
        if data.mode == "Reaction Practice": Rxn.init(data.RxnData)

def keyPressed(event, data):
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    if data.mode == "Reaction Practice": Rxn.redrawAll(canvas, data.RxnData)
    else:
        drawMMButtons(canvas, data)

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
    data.RxnData = Struct()
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