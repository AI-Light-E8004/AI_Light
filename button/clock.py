from tkinter import * 
import time 

root = Tk()
root.title("my title)")
root.geometry("600x400")

def clock():
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")

    my_label.config(text=hour + ":" + minute + ":" + second)
    my_label.after(1000, clock)
def update():
    my_label.config(text= "new text")

my_label = Label(root, text= "", font=("Helvetica", 48),fg="green")
my_label.pack(pady = 20)

clock()