import pyvisa as pv
import tkinter as tk
from tkinter import ttk


class VISAInstrument:
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

    def create_widget(self, frame):
        rm = pv.ResourceManager()
        self._widget = InstrWidget(frame, self, rm.list_resources())
        print(f"{self._instr} widget successfully created")

    def set_address(self, address):
        self._address = address

    def connect(self):
        rm = pv.ResourceManager()
        if self._address:
            try:
                self._instr = rm.open_resource(self._address)
                print(f"Connected instrument: {self._instr.query('*IDN?')}{self._instr}")
            except:
                print("Failed to connect the instrument. Check if the intended VISA address is listed below:")
                print(rm.list_resources())
        else:
            print("Failed to connect the instrument. You must specify a VISA address within:")
            print(rm.list_resources())

    def disconnect(self):
        try:
            self._instr.close()
            print(f"Disconnected instrument: {self._instr}")
            self._instr   = None
            self._address = None
        except:
            print(f"Failed to disconnect: {self._instr}")

class InstrWidget:
    def __init__(self, frame, instrument, address_list=[]):
        self._instrument = instrument

        self._label  = ttk.Label(frame, text=f"{self._instrument.name}:", width=10)
        self._combo  = ttk.Combobox(frame, values=address_list, width=40)
        self._button = ttk.Button(frame, text="Connect", command=self._button_clicked)

        options = {'sticky': tk.W, 'padx': 5, 'pady': 5}
        self._label.grid(row=0, column=0, **options)
        self._combo.grid(row=0, column=1, **options)
        self._button.grid(row=0, column=2, **options)

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