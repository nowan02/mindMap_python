from tkinter import *

mainWindow = Tk()
mainWindow.geometry("1280x720")

canvasFrame = Frame(width=1000, height=800)
canvasFrame.pack(expand=True,fill=BOTH)
canvas = Canvas(canvasFrame, bg="lightgrey", confine=False, width=8196, height=8196, scrollregion=(0,0,8196,8196)) 
hbar = Scrollbar(canvasFrame, orient=HORIZONTAL)
vbar = Scrollbar(canvasFrame, orient=VERTICAL)
hbar.pack(side=BOTTOM, fill=X)
vbar.pack(side=RIGHT, fill=Y)
hbar.config(command=canvas.xview)
vbar.config(command=canvas.yview)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

class mindNode:
    def __init__(self, x, y, height, width, color, textColor, text):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.textColor = textColor
        self.text = text
        self.children = list[mindNode]

root = mindNode(0,0,200,100,"red","white","I am root")
selected = root

canvas.create_rectangle(root.x,root.y,root.x+root.width,root.y+root.height,fill=root.color)
canvas.create_text(root.x+(root.width/2),root.y+(root.height/2),
font=("Arial 15"), fill=root.textColor, text=root.text, width=root.width)

def collisionDetection(event:Event, node:mindNode):
    if((node.x <= event.x and event.x <= node.x+node.width)
    and (node.y <= event.y and event.y <= node.y+node.height)):
        return True
    return False

def search(event:Event, parentNode:mindNode):
    global selected
    if(collisionDetection(event, parentNode) == True):
        selected = parentNode
        print("katt")
        return
    else:
        if(parentNode.children.count != 0):
            for i in parentNode.children:
                search(event, parentNode.children[i])

def select(event):
    global root
    if(event.num == 1):
        search(event, root)
             
def create(event):
    pass
    

canvas.bind("<Button>", select)
canvas.bind("<Shift-Button>", create)

canvas.pack(expand=True, fill=BOTH)
mainWindow.mainloop()
