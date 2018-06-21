from tkinter import *
def callback():
    print('You clicked the button!')

def main():

    OPTIONS = [
        "Europe",
        "European Union",
        "Central & Eastern Europe",
        "Asia",
        "Middle East",
        "South Asia",
        "South East Asia",
        "East Asia(without Middle East)",
        "Americas",
        "North America",
        "Latin America",
        "Central America & Caribbe",
        "USA",
        "Oceania",
        "Arab world",
        "Africa",
        "North Africa",
        "Sub-Saharan Africa",
        "World",
        "Asia/Pacific",
        "Eurasia"
    ]


    root = Tk()
    root.title("WebCrawling")
    # root.configure(background='white')
    root.geometry("300x80")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    lbl_username = Label(root, text = "Select a Region :")
    lbl_username.grid(row=0, column=0)

    variable = StringVar(root)
    variable.set(OPTIONS[0]) # default value
    w = OptionMenu(root, variable, *OPTIONS)
    w.grid(row=0,column=1)

    MyButton = Button(root, text="Submit", width=10, command=callback)
    MyButton.grid(row=2, column=1)





    root.mainloop()




    # root = Tk()
    # root.title("Python: Simple Login Application")
    # width = 400
    # height = 280
    # screen_width = root.winfo_screenwidth()
    # screen_height = root.winfo_screenheight()
    # x = (screen_width/2) - (width/2)
    # y = (screen_height/2) - (height/2)
    # root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    # root.resizable(0, 0)




main()
