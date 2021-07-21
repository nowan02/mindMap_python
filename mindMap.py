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
    def __init__(self, x, y, node, text):
        self.x = x
        self.y = y
        self.nodeId = node
        self.textId = text
        self.children = []

def search(parentNode, searchId):
    global selected
    if(parentNode.nodeId == searchId):
        selected = parentNode
        return
    else:
        for n in parentNode.children:
            search(n, searchId)

def nodeSelect(event):
    nodeId = event.widget.find_withtag('current')[0]
    print("mindNode with id:", nodeId, "clicked")
    search(rootNode, nodeId)
    print(selected.nodeId)

def addNode(x, y, width, height, text, color, textColor):
    rectangle = canvas.create_rectangle(x, y, x+width, y+height, fill=color)
    canvas.tag_bind(rectangle,"<Button>",nodeSelect)
    text = canvas.create_text(x+width/2, y+width/2, font=("Arial",15), text=text, fill=textColor, width=width)
    newNode = mindNode(x, y, rectangle,text)
    selected.children.append(newNode)

root = canvas.create_rectangle(0,0,200,100,fill="red")
rootText = canvas.create_text(100,50,font=("Arial",15),fill="white",width=100,text="I am root")
rootNode = mindNode(0, 0, root, rootText)
selected = rootNode
canvas.tag_bind(root,"<Button>",nodeSelect) 

def clickWrapper(event):
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

    def confirm():
        if(tisWidthEntry.get() != "" and tisHeightEntry.get() != "" and tisColorEntry.get() != "" and tisTextColorEntry.get() != "" and tisTextEntry.get() != ""):
            addNode(event.x, event.y, int(tisWidthEntry.get()), int(tisHeightEntry.get()), tisTextEntry.get(), tisColorEntry.get(), tisTextColorEntry.get())
            editor.destroy()
        else:
            print("No entry")

    confirmButton = Button(editor, text="Confirm", command=confirm)
    confirmButton.pack()

canvas.bind("<Shift-Button>", clickWrapper)

canvas.pack(expand=True, fill=BOTH)
mainWindow.mainloop()