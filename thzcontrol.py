import tkinter as tk
from tkinter import ttk
from instruments import Lockin, Cernox, KBD101
from experiment import Prefs, Measurement


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.geometry('1180x700+0+0')
        self.title('THzControl')
        self.resizable(False, False)
        self.tk.call('tk', 'scaling', 2.0)
        
        
if __name__ == '__main__':
    app = App()
    
    # Frames:
    instr_frame = ttk.Frame(app)
    prefs_frame = ttk.Frame(app)
    #measu_frame = ttk.Frame(app)
    
    # Instruments:
    lock_in      = Lockin()
    thermometer = Cernox()
    #multimeter = MultimeterOld("USB0::0x0957::0x0607::MY47027685::INSTR")
    delay_line  = KBD101("28250877")
    lock_in.create_widget(instr_frame, 0)
    thermometer.create_widget(instr_frame, 1)
    delay_line.create_widget(instr_frame, 2)
    
    # Preferences:
    prefs = Prefs(prefs_frame)
   
    # Measurement:
    #measu = Measurement(measu_frame, multimeter, delay_line, prefs)
    
    # Grid frames:
    instr_frame.grid(row=0, column=0, sticky='W', pady=10)
    prefs_frame.grid(row=1, column=0, sticky='W', pady=10)
    #measu_frame.grid(row=2, column=0, sticky='W', pady=10)
    
    # App better visual dpi:
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        app.mainloop()