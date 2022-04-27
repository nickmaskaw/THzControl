import os
import tkinter as tk
from tkinter import ttk


class Preferences:
    PRESET_FOLDER = './preset'
    PRESET_FILE = 'prefs.txt'

    def __init__(self):
        self._check_preset_folder()

    def _check_preset_folder(self):
        if not os.path.exists(self.PRESET_FOLDER): os.makedirs(self.PRESET_FOLDER)
        print("Checked preferences preset folder")


class PreferencesWidget:
    def __init__(self, frame):
        pass


class Item:
    def __init__(self, frame, name, unit):
        self._name  = name
        self._unit  = unit
        self._value = None
        self._container = ttk.Frame(frame)

    @property
    def name(self): return self._name
    @property
    def unit(self): return self._unit
    @property
    def container(self): return self._container


class Entry(Item):
    def __init__(self, frame, name, unit, box_width, type_=str):
        super().__init__(frame, name, unit)
        self._value = tk.StringVar(value="")
        self._type  = type_

        self._label     = ttk.Label(self.container, text=f"{self.name}:", width=10)
        self._valuebox  = ttk.Entry(self.container, textvariable=self._value, justify='right', width=box_width)
        self._unitlabel = ttk.Label(self.container, text=self.unit, width=6)

        options = {'sticky': tk.W, 'padx': 5, 'pady': 5}
        self._label.grid(row=0, column=0, **options)
        self._valuebox.grid(row=0, column=1, **options)
        self._unitlabel.grid(row=0, column=2, **options)

    @property
    def value(self): return self._type(self._value)

    def set_value(self, value):
        self._value.set(value)

    def enable(self):
        self._valuebox['state'] = 'normal'

    def disable(self):
        self._valuebox['state'] = 'disabled'


class Combo(Item):
    def __init__(self, frame, name, unit, box_width):