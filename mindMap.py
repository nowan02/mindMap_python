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

canvas.create_rectangle(root.x,root.y,root.x+root.width,root.y+root.height,fill=root.color)
canvas.create_text(root.x+(root.width/2),root.y+(root.height/2),
font=("Arial 15"), fill=root.textColor, text=root.text, width=root.width)

canvas.pack(expand=True, fill=BOTH)
mainWindow.mainloop()
