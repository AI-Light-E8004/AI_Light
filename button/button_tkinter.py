# import tkinter as tk
from tkinter import *
root = Tk()
root.geometry('600x400')

colour1 = '#020f12'
colour2 = '#05d7ff'
colour3 = '#65e7ff'
colour4 = 'black'

main_frame = Frame(
    root, bg=colour1, pady=40)
main_frame.pack(fill=BOTH, expand=True)
main_frame.columnconfigure(0, weight=1) 
main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=1) 


button1 = Button(
    main_frame,
    background=colour2,
    foreground=colour4,
    activebackground=colour3,
    activeforeground=colour4,
    highlightthickness=2,
    highlightcolor='WHITE' ,
    width=26,
    height=3,
    border=0,
    cursor='hand1',
    text='Click here to speak to the oracle',
    font=('Helvetica', 16, 'bold')
    )      
button1.grid(column=0, row=0)

def bt1_enter(event):
    button1.config(
        highlightbackground=colour3
    )
def bt1_leave(event):
    button1.config(
        highlightbackground=colour4
    )

def switch_Windows(self):
    
    pass

button1.bind('<Enter>', bt1_enter)
button1.bind('<Leave>', bt1_leave) 


root.mainloop()