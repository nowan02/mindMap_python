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
    search(root, nodeId)
    print("mindNode with id:", selected, "selected")

class mindNode:
    def __init__(self, x, y, text, textColor, rectColor):

        width = 200
        height = 100

        if(len(text) > 200):
            height += 20 

        self.nodeId = canvas.create_rectangle(x, y, x+width, y+height, fill=rectColor)
        self.textId = canvas.create_text(x+width/2, y+height/2, font=("Arial",15), text=text, fill=textColor, width=width-10)
        canvas.tag_bind(self.nodeId,"<Button>",nodeSelect)
        self.children = []

root = mindNode(0, 0, "I am root", "white", "red")
selected = root

def wrapper(event):
    editor = Toplevel(mainWindow)
    editor.title("Node editor")
    editor.geometry("300x300")

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
        if(tisColorEntry.get() != "" and tisTextColorEntry.get() != "" and tisTextEntry.get() != ""):
            selected.children.append(mindNode(event.x, event.y, tisTextEntry.get(), tisTextColorEntry.get(), tisColorEntry.get()))
            editor.destroy()
        else:
            print("No entry")

    confirmButton = Button(editor, text="Confirm", command=confirm)
    confirmButton.pack()

canvas.pack()
mainWindow.mainloop()