import os
import pyvisa as pv
import tkinter as tk
from tkinter import ttk


class VISAInstrument:
    PRESET_FOLDER = './preset'
    
    def __init__(self, name):
        self._name    = name
        self._address = None
        self._instr   = None
        self._widget  = None

    @property
    def name(self): return self._name
    @property
    def address(self): return self._address
    @property
    def instr(self): return self._instr
    @property
    def widget(self): return self._widget
    @property
    def idn(self):
        if self.instr: return self.instr.query('*IDN?')
        else:          return "No instrument"
    @property
    def is_connected(self): return True if self.instr else False
    
    def _save_preset(self):
        if not os.path.exists(self.PRESET_FOLDER): os.makedirs(self.PRESET_FOLDER)
        with open(f'{self.PRESET_FOLDER}/{self.name}_address', 'w') as file:
            file.write(self.address)
        print(f"Saved {self.name} address to preset folder")
        
    def _load_preset(self):
        try:
            with open(f'{self.PRESET_FOLDER}/{self.name}_address') as file:
                self.widget.combo_set(file.readlines()[0])
            print(f"Loaded {self.name} address preset")
        except:
            print(f"No {self.name} address found in preset folder")

    def create_widget(self, frame, row):
        rm = pv.ResourceManager()
        self._widget = InstrWidget(frame, row, self, rm.list_resources())
        print(f"{self.name} widget successfully created")
        self._load_preset()

    def set_address(self, address):
        self._address = address

    def connect(self):
        rm = pv.ResourceManager()
        if self._address:
            try:
                self._instr = rm.open_resource(self._address)
                self.instr.read_termination  = '\n'
                self.instr.write_termination = '\n'
                print(f"Connected {self.name}: {self.idn} ({self.instr})")
                self._save_preset()
            except:
                print(f"Failed to connect the {self.name}")
        else:
            print(f"Failed to connect the {self.name}. You must specify a VISA address within:")
            print(rm.list_resources())

    def disconnect(self):
        try:
            self.instr.close()
            print(f"Disconnected the {self.name} ({self.instr})")
            self._instr   = None
            self._address = None
        except:
            print(f"Failed to disconnect the {self.name} ({self.instr})")


class InstrWidget:
    def __init__(self, frame, row, instrument, address_list=[]):
        self._instrument = instrument

        self._label  = ttk.Label(frame, text=f"{self._instrument.name}:", width=10)
        self._combo  = ttk.Combobox(frame, values=address_list, width=40)
        self._button = ttk.Button(frame, text="Connect", command=self._button_clicked)

        options = {'sticky': tk.W, 'padx': 5, 'pady': 5}
        self._label.grid(row=row, column=0, **options)
        self._combo.grid(row=row, column=1, **options)
        self._button.grid(row=row, column=2, **options)

    def _button_clicked(self):
        if self._button['text'] == "Connect":
            self._instrument.set_address(self._combo.get())
            self._instrument.connect()
            if self._instrument.instr:
                self._combo['state'] = 'disabled'
                self._button['text'] = "Disconnect"
        elif self._button['text'] == "Disconnect":
            self._instrument.disconnect()
            if not self._instrument.instr:
                self._combo['state'] = 'normal'
                self._button['text'] = "Connect"
                
    def combo_set(self, value):
        self._combo.set(value)