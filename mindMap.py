from tkinter import *

mainWindow = Tk()
mainWindow.title("Mindmap")
mainWindow.geometry("1280x720")

canvasFrame = Frame(width=1000, height=800)
canvasFrame.pack(expand=True, fill=BOTH)
canvas = Canvas(canvasFrame, bg="lightgrey", confine=False,
                width=8196, height=8196, scrollregion=(0, 0, 8196, 8196))
hbar = Scrollbar(canvasFrame, orient=HORIZONTAL)
vbar = Scrollbar(canvasFrame, orient=VERTICAL)
hbar.pack(side=BOTTOM, fill=X)
vbar.pack(side=RIGHT, fill=Y)
hbar.config(command=canvas.xview)
vbar.config(command=canvas.yview)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)


class mindNode:
    x:int
    y:int
    height:int
    width:int
    color:str
    textColor:str
    text:str
    children:any
    def __init__(self, x, y, height=0, width=0, color="", textColor="", text=""):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.textColor = textColor
        self.text = text
        self.children = [mindNode]

root = mindNode(0, 0, 200, 100, "red", "white", "I am root")
selected = root

canvas.create_rectangle(root.x, root.y, root.x+root.width,
                        root.y+root.height, fill=root.color)
canvas.create_text(root.x+(root.width/2), root.y+(root.height/2),
                   font=("Arial 15"), fill=root.textColor, text=root.text, width=root.width)


def collisionDetection(event:Event, node: mindNode):
    return(node.x <= event.x and event.x <= node.x+node.width) and (node.y <= event.y and event.y <= node.y+node.height)


def search(event: Event, parentNode: mindNode):
    global selected
    if(collisionDetection(event, parentNode)):
        selected = parentNode
        print("katt")
        return

    for i in parentNode.children:
        search(event, parentNode.children[i])

def select(event: Event):
    global root
    if(event.num == 1):
        search(event, root)

def reDraw(node:mindNode):
    canvas.delete("all")
    canvas.create_rectangle(node.x, node.y, node.x+node.width,
                    node.y+node.height, fill=node.color)
    canvas.create_text(node.x+(node.width/2), node.y+(node.height/2),
                font=("Arial 15"), fill=node.textColor, text=node.text, width=node.width)
    
    for n in node.children:
        reDraw(n)      

def create(event:Event):
    editor = Toplevel(mainWindow)
    editor.title("Node editor")
    editor.geometry("300x300")

    tisWidth = Label(editor, text="Width")
    tisWidth.config(font=('Arial', 14))
    tisWidth.pack()
    tisWidthEntry = Entry(editor)
    tisWidthEntry.pack()

    tisHeight = Label(editor, text="Height")
    tisHeight.config(font=('Arial', 14))
    tisHeight.pack()
    tisHeightEntry = Entry(editor)
    tisHeightEntry.pack()

    tisColor = Label(editor, text="Color")
    tisColor.config(font=('Arial', 14))
    tisColor.pack()
    tisColorEntry = Entry(editor)
    tisColorEntry.pack()

    tisTextColor = Label(editor, text="Text Color")
    tisTextColor.config(font=('Arial', 14))
    tisTextColor.pack()
    tisTextColorEntry = Entry(editor)
    tisTextColorEntry.pack()

    tisText = Label(editor, text="Text")
    tisText.config(font=('Arial', 14))
    tisText.pack()
    tisTextEntry = Entry(editor)
    tisTextEntry.pack()

    newNode = mindNode(event.x, event.y)

    def confirm():
        
        selected.children.append(newNode)
        reDraw(root)

    confirmButton = Button(editor, text="Confirm", command=confirm)
    confirmButton.pack()


canvas.bind("<Button>", select)
canvas.bind("<Shift-Button>", create)

canvas.pack(expand=True, fill=BOTH)
mainWindow.mainloop()
