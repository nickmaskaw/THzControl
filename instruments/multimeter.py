import pyvisa as pv
import tkinter as tk
from tkinter import ttk


class Multimeter:
    def __init__(self, default_address):
        self._default_address = default_address
        self._instr           = None
        self._widget          = False
        self._connected       = False
        
    def is_connected(self): return self._connected
        
    def create_widget(self, frame, row):
        if not self._widget:
            self._widget = True
            default_address = self._default_address
            options = {'sticky': tk.W, 'padx': 5, 'pady': 5}

            self._label   = ttk.Label(frame, text="Multimeter:", width=10)
            self._address = tk.StringVar(value=default_address)
            self._entry   = ttk.Entry(frame, textvariable=self._address, width=40)
            self._button  = ttk.Button(frame, text="Connect", command=self._button_clicked)
            self._value   = tk.StringVar(value="")
            self._visual  = ttk.Entry(frame, textvariable=self._value, width=20, state='disabled')
            self._get_btn = ttk.Button(frame, text="Get", command=self._button_get, state='disabled')

            self._label.grid(row=row, column=0, **options)
            self._entry.grid(row=row, column=1, **options)
            self._button.grid(row=row, column=2, **options)
            self._visual.grid(row=row, column=3, **options)
            self._get_btn.grid(row=row, column=4, **options)
            
            print("Multimeter widget successfully created")
        else:
            print("Multimeter widget already exists")
        
    def _button_clicked(self):
        if self._button['text'] == "Connect":
            self.connect()
        elif self._button['text'] == "Disconnect":
            self.disconnect()
    
    def _button_get(self):
        self._value.set(float(self.get_meas()))
        
    def widget_enable(self):
        if self._widget and self._connected:
            self._button['state']  = 'normal'
            self._visual['state']  = 'normal'
            self._get_btn['state'] = 'normal'
        print("Multimeter widget enabled")
            
    def widget_disable(self):
        if self._widget and self._connected:
            self._button['state']  = 'disabled'
            self._visual['state']  = 'disabled'
            self._get_btn['state'] = 'disabled'
        print("Multimeter widget disabled")
                                   
    def connect(self, manual_address=None):
        VISA_ADDRESS = self._address.get() if not manual_address else manual_address
        rm = pv.ResourceManager()
        try:
            self._instr     = rm.open_resource(VISA_ADDRESS)
            self._connected = True
            if self._widget:
                self._button['text']   = "Disconnect"
                self._entry['state']   = 'disabled'
                self._visual['state']  = 'normal'
                self._get_btn['state'] = 'normal'
                self._button_get()
            print(f"Connected multimeter: {self._instr.query('*IDN?')}{self._instr}")
        except:
            print("Failed to connect the multimeter. Check if the intended VISA address is listed below:")
            print(rm.list_resources())
            
    def disconnect(self):
        try:
            self._instr.close()
            self._connected = False
            if self._widget:
                self._button['text']   = "Connect"
                self._entry['state']   = 'normal'
                self._visual['state']  = 'disabled'
                self._get_btn['state'] = 'disabled'
            print("Disconnected the multimeter")
        except:
            print("Failed to disconnect the multimeter")
            
    def get_meas(self):
        return self._instr.query('MEAS?')