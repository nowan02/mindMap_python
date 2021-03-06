from tkinter import *
from tkinter import messagebox
from io import *

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
    print("mindNode with id:", selected.nodeId, "selected")

class mindNode:
    def __init__(self, x, y, text, textColor, rectColor, parent):

        width = 200
        height = 100

        if(len(text) >= 200):
            height += 20 

        self.text = text
        self.textColor = textColor
        self.rectColor = rectColor
        self.parent = parent
        self.deleted = False
        self.nodeId = canvas.create_rectangle(x, y, x+width, y+height, fill=rectColor)
        self.textId = canvas.create_text(x+width/2, y+height/2, font=("Arial",15), text=text, fill=textColor, width=width-10)
        canvas.tag_bind(self.nodeId,"<Button>",nodeSelect)
        self.children = []
        
        if(self.parent != 1):
            parX, parY, parW, parH = canvas.coords(self.parent.nodeId)
            selfX, selfY, selfW, selfH = canvas.coords(self.nodeId)

            lineY = selfY + ((selfH - selfY) / 2)
            lineH = parY + ((parH - parY) / 2)

            if(parX < selfX): # parent to the LEFT
                lineX = selfX
                lineW = parW
                if(selfX < parW): # if node X value is between parent X and width
                    lineX = selfX + ((selfW - selfX) / 2)
                    lineW = parX + ((parW - parX) / 2)
                    if(parY < selfY): # parent is OVER
                        lineY = selfY
                        lineH = parH
                    else:   # parent is UNDER
                        lineY = parY
                        lineH = selfH
            else:             # parent to the RIGHT
                lineX = selfW
                lineW = parX
            
            self.conLine = canvas.create_line(lineX, lineY, lineW, lineH)

    def delete(self):
        canvas.delete(self.textId, self.nodeId)
        self.deleted = True
        for n in self.children:
            n.delete()

    def deleteForGood(self):
        if(self.deleted == True):
            self.parent.children.remove(self)
        for n in self.children:
            n.deleteForGood()

    def reDraw(self):
        for n in self.children:
            x,y,w,h = canvas.coords(n.nodeId)
            n.nodeId = canvas.create_rectangle(x, y, w, h, fill = self.rectColor)
            n.textId = canvas.create_rectangle(x+w/2,y+h/2, font=("Arial",15), text=self.text, fill=self.textColor, width=w-10)

def create(parameter):
    try:
        newNode = mindNode(parameter[0],parameter[1],parameter[2],parameter[3],parameter[4], selected)
    except:
        messagebox.showerror("Color code error", f'An invalid color value was used, substituting with white and black')
        newNode = mindNode(parameter[0],parameter[1],parameter[2],"black","white", selected)
    selected.children.append(newNode)

def edit(parameter):
    _,_,width,height = canvas.coords(selected.nodeId)
    w = width - parameter[0]
    h = height - parameter[1]
    selected.delete()
    try:
        selected.nodeId = canvas.create_rectangle(parameter[0], parameter[1], width, height, fill = parameter[4])
        selected.textId = canvas.create_text(parameter[0]+w/2,parameter[1]+h/2, font=("Arial",15), text=parameter[2], fill=parameter[3], width=w-10)
    except:
        messagebox.showerror("Color code error", f'An invalid color value was used, substituting with white and black')
        selected.nodeId = canvas.create_rectangle(parameter[0], parameter[1], width, height, fill = "white")
        selected.textId = canvas.create_text(parameter[0]+w/2,parameter[1]+h/2, font=("Arial",15), text=parameter[2], fill="black", width=w-10)

def editorWindow(x,y,callback):
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

    def editorCallback():
        param = [x, y, tisTextEntry.get(), tisTextColorEntry.get(), tisColorEntry.get()]
        callback(param)

    confirmButton = Button(editor,text="Confirm",command=editorCallback)
    confirmButton.pack()

root = mindNode(0, 0, "I am root", "white", "red", 1)
print(root.nodeId)
selected = root

def createWrapper(event):
    editorWindow(event.x,event.y,create)

def editWrapper(event):
    x,y,_,_ = canvas.coords(selected.nodeId)
    editorWindow(x,y,edit)

canvas.bind("<Shift-Button>", createWrapper)
canvas.bind("<Control-Button>", editWrapper)

def save():
    saveName = "save.txt"
    saveFile = open(saveName, "w")

    def recurse(node:mindNode, doc):
        x,y,_,_ = canvas.coords(node.nodeId)
        if(x != 0 and y != 0):
            doc.write(f'{int(x)},{int(y)},{node.text},{node.textColor},{node.rectColor},{node.parent.nodeId}')

        for n in node.children:
            recurse(n, doc)

    recurse(root, saveFile)
    saveFile.close()
    mainWindow.quit()

def load():
    saveFile = open("save.txt", "r")
    global selected
    linenum = 1
    while(True):
        line = saveFile.readline()
        if(not line):
            break
        param = line.split(",")
        print(param)
        if(param[5] == 1):
            selected = root
        
        try:
            param[0] = int(param[0])
            param[1] = int(param[1])
        except ValueError:
            messagebox.showerror('Coordinate error', f'An invalid value for X or Y was found in the save file on line {linenum}, please check save.txt for possible errors')
            break

        try:
            node = mindNode(param[0],param[1],param[2],param[3],param[4],selected)
            node.parent.children.append(node)
        except:
            messagebox.showerror("Color code error", f'An invalid color value was found in the save file on line {linenum}, substituting with white and black')
            node = mindNode(param[0],param[1],param[2],"black","white",selected)
        selected = node

        linenum+=1
    saveFile.close()

saveButton = Button(canvasFrame,text="Save and Quit",command=save)
saveButton.pack()
loadButton = Button(canvasFrame, text="Load from text file",comman=load)
loadButton.pack()
canvas.pack()
mainWindow.mainloop()