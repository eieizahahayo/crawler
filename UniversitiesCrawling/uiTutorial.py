from tkinter import *

root = Tk()

# topFrame = Frame(root)
# topFrame.pack()
# bottomFrame = Frame(root)
# bottomFrame.pack(side=BOTTOM)
# button1 = Button(topFrame,text="Button 1",fg="red")
# button1.pack(side=LEFT)
# button2 = Button(topFrame,text="Button 2",fg="yellow")
# button2.pack(side=LEFT)
# button3 = Button(topFrame,text="Button 3",fg="blue")
# button3.pack(side=LEFT)
# button4 = Button(bottomFrame,text="Button 4",fg="green")
# button4.pack(side=RIGHT)


one = Label(root,text="One",bg="green",fg="white")
one.pack()
two = Label(root,text="Two",bg="yellow",fg="white")
two.pack(fill=X)
two = Label(root,text="Two",bg="orange",fg="white")
two.pack(side=LEFT,fill = Y)


root = mainloop()
