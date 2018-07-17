from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from uniCrawling import *
from PIL import ImageTk, Image
import os
from time import sleep




def main():
    def browse():
        file =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        fileEntry.config(text = file)
        return file

    def begin(file,name):
        print("File : " + file)
        print("Name : " + name)
        crawling(file,name)
        img2 = ImageTk.PhotoImage(Image.open("bg2.jpg"))
        panel.configure(image=img2)
        panel.image = img2




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

    nameText = Label(group, text="Enter the name : ")
    nameEntry = Entry(group)


    nameText.grid(row=0, sticky=E)
    nameEntry.grid(row=0, column=1)

    fileEntry = Label(group)
    fileButton = Button(group, text="Choose file", width=10, command=browse)
    fileButton.grid(row=1,sticky=E)
    fileEntry.grid(row=1, column=1)

    MyButton = Button(group, text="Submit", width=10,
        command=lambda:begin(fileEntry.cget("text"),nameEntry.get()))
    MyButton.grid(columnspan=2)

    root.mainloop()

main()
