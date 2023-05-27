from tkinter import *

root = Tk()
root.geometry("400x400")
varg = StringVar()

output = "Ayo"
label = Label( root, textvariable=varg)
print(type(varg))

varg.set(output)
label.pack()
root.mainloop()

