from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from main import *
from PIL import ImageTk, Image
import os
from time import sleep




def main():
    OPTIONS = [
        "Wiley",
        "Springer",
        "Europe PMC",
        "Science Direct",
        "arXiv"
    ]

    def begin(file,name,choice):
        craw(file,name,choice)

    root = Tk()
    root.config(height=300, width=600,background='white')
    root.resizable(width=False, height=False)
    root.title("Universities Crawling")

    img = ImageTk.PhotoImage(Image.open("bg1.jpg"))
    panel = Label(root, image = img)
    panel.pack(side = "top", fill = "both", expand = "yes")

    group = LabelFrame(root, text="Input", padx=5, pady=5)
    group.pack(padx=10, pady=10)
    group.place(relx=0.5, rely=0.5, anchor=CENTER)

    choiceLabel = Label(group,text="Select database : ")
    choiceLabel.grid(row=0,column=0)

    variable = StringVar(group)
    variable.set(OPTIONS[0]) # default value
    w = OptionMenu(group, variable, *OPTIONS)
    w.grid(row=0,column=1)

    keyText = Label(group,text="Enter keyword :")
    keyEntry = Entry(group)
    keyText.grid(row=1, sticky=E)
    keyEntry.grid(row=1, column=1)

    nameText = Label(group, text="Enter file name : ")
    nameEntry = Entry(group)
    nameText.grid(row=2, sticky=E)
    nameEntry.grid(row=2, column=1)


    MyButton = Button(group, text="Submit", width=10,
        command=lambda:begin(keyEntry.get(),nameEntry.get(),variable.get()))
    MyButton.grid(columnspan=2)

    root.mainloop()

main()
