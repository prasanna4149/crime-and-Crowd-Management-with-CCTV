import tkinter as tk
from tkinter import *
from tkinter import ttk

class karl( Frame ):
    def __init__( self ):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("Karlos")
        self.button1 = Button( self, text = "CLICK HERE", width = 25,
                               command = self.new_window )
        self.button1.grid( row = 0, column = 1, columnspan = 2, sticky = W+E+N+S )
    def new_window(self):
        self.newWindow = karl2()

class karl2(Frame):     
    def __init__(self):
        new =tk.Frame.__init__(self)
        new = Toplevel(self)
        new.title("karlos More Window")
        new.button = tk.Button(  text = "PRESS TO CLOSE", width = 25,command = self.close_window )
        new.button.pack()
        new.button1 = Button( self, text = "CLICK HERE", width = 25,command = self.wow_window )
    def wow_window(self):
        self.wowWindow = karl22()
        

class karl22():
    def __init__(self):
        wow =tk.Frame.__init__(self)
        wow = Toplevel(self)
        wow.title("karlos More Window")
        wow.button = tk.Button(  text = "PRESS TO CLOSE", width = 25,command = self.close_window )
        wow.button.pack()
    def close_window(self):
        self.destroy()
def main(): 
    karl().mainloop()
if __name__ == '__main__':
    main()