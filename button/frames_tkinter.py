from tkinter import *
import time

root = Tk()
# root.geometry('600x400')

colour1 = '#020f12'
colour2 = '#05d7ff'
colour3 = '#65e7ff'
colour4 = 'black'

def raise_frame(frame):
    frame.tkraise()



f1 = Frame(
    root, bg=colour1, pady=40)
f1.pack(fill=BOTH, expand=True)
f1.columnconfigure(0, weight=1) 
f1.rowconfigure(0, weight=1)
f1.rowconfigure(1, weight=1) 

f2 = Frame(
    root, bg=colour1, pady=40)
f3 = Frame(
    root, bg=colour1, pady=40)
f4 = Frame(
    root, bg=colour1, pady=40)

for frame in (f1, f2, f3, f4):

    frame.grid(row=1000, column=1000, sticky='news')

label1 = Label(f1,
                text='FRAME 1').pack(side=TOP)
button1 = Button(f1, 
                background= colour2,
                foreground= colour4,
                activebackground= colour3,
                activeforeground= colour4,
                width=26,
                height = 3, 
                text='Click here to speak to the oracle', 
                command=lambda:raise_frame(f2)).pack(side=TOP)


Label(f2, text='You have 5 seconds to speak your mind').pack()
Button(f2, 
        background= colour2,
        foreground= colour4,
        activebackground= colour3,
        activeforeground= colour4,
        width=26,
        height = 3 , text='After 5s click here to let oracle know you finished', command=lambda:raise_frame(f3)).pack(side=TOP)


Label(f3, text='The oracle is thinking').pack()
Button(f3, text='Wait for oracle to think', command=lambda:raise_frame(f4)).pack()

Label(f4, text='Displaying the result').pack()
Button(f4, text='Go back home', command=lambda:raise_frame(f1)).pack()


# raise_frame(f1)
# root.mainloop()

if __name__ == "__main__":
    raise_frame(f1)
    root.mainloop()
    pass
