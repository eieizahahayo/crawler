from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import filedialog

def callback():
    print('You clicked the button!')





def main():
    def browse():
        file =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        return file

    root = Tk()
    root.config(height=300, width=600)
    root.title("Universities Crawling")

    group = LabelFrame(root, text="Group", padx=5, pady=5)
    group.pack(padx=10, pady=10)
    group.place(relx=0.5, rely=0.5, anchor=CENTER)

    nameText = Label(group, text="Enter the name : ")
    nameEntry = Entry(group)

    nameText.grid(row=0, sticky=E)
    nameEntry.grid(row=0, column=1)

    fileButton = Button(group, text="Choose file", width=10, command=browse)
    fileButton.grid(row=1,sticky=E)
    fileEntry = Label(group)
    fileEntry.grid(row=1, column=1)

    MyButton = Button(group, text="Submit", width=10, command=callback)
    MyButton.grid(columnspan=2)

    root.mainloop()

main()
