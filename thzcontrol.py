import tkinter as tk
from tkinter import ttk
from instruments import Lockin, Cernox, KBD101
from experiment import Parameters


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.geometry('1180x700+0+0')
        self.title('THzControl')
        self.resizable(False, False)
        self.tk.call('tk', 'scaling', 2.0)
        
    def set_mainloop(self):
        # App better visual dpi:
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        finally:
            self.mainloop()
        
        
if __name__ == '__main__':
    app = App()
    
    # Frames:
    instr_frame = ttk.Frame(app)
    param_frame = ttk.Frame(app)
    
    # Instruments:
    lock_in     = Lockin()
    thermometer = Cernox()
    delay_line  = KBD101("28250877")
    
    # Instrument widgets:
    lock_in.create_widget(instr_frame, 0)
    thermometer.create_widget(instr_frame, 1)
    delay_line.create_widget(instr_frame, 2)
    
    # Parameters:
    parameters = Parameters()

    # Parameters widget:
    parameters.create_widget(param_frame)
   
    # Measurement:
    
    # Grid frames:
    instr_frame.grid(row=0, column=0, sticky='W', pady=10)
    param_frame.grid(row=1, column=0, sticky='W', pady=10)
    
    app.set_mainloop()
    
    