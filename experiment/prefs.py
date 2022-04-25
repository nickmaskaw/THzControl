import tkinter as tk
from tkinter import ttk
from pandas import DataFrame, read_csv
import os



class Prefs:
    PRESET_FOLDER = './preset'
    PRESET_FILE   = 'prefs.txt'
    
    def __init__(self, container):
        self._widget_create(container)
        self._check_preset_folder()
        self.load_preset()
    
    def __repr__(self):
        dict_  = self.__dict__
        string = ''
        for key in dict_:
            string += f"{key}: {dict_[key]}\n"
        return string
    
    @property
    def table(self):
        dici = self.__dict__
        keys = list(dici)
        vals = list(dici[key].value for key in keys)
        unit = list(dici[key].unit for key in keys)
        return DataFrame({'value': vals, 'unit': unit}, index=keys)
    @property
    def values(self): return self.table.value
    @property
    def units(self): return self.table.unit
    
    def _check_preset_folder(self):
        if not os.path.exists(Prefs.PRESET_FOLDER): os.makedirs(Prefs.PRESET_FOLDER)
        print("Checked parameters preset folder")
    
    def save_preset(self):
        self.table.to_csv(f"{Prefs.PRESET_FOLDER}/{Prefs.PRESET_FILE}", sep='\t')
        print("Saved parameters preset")
        
    def load_preset(self):
        try:
            table = read_csv(f"{Prefs.PRESET_FOLDER}/{Prefs.PRESET_FILE}", sep='\t', index_col=0).fillna('')
            dici  = self.__dict__
            for key in list(dici):
                if not key == 'fast':
                    dici[key].set_value(table.value[key])
            print("Loaded parameter presets")
        except:
            print("ERROR: Could not load parameter presets")
            
    def save(self, folder, file):
        self.table.to_csv(f"{folder}/{file}___info.txt", sep='\t')
            
    
    def _widget_create(self, container):
        self.start   = Entry(container, 'Start', 'mm', 75, mark="*")
        self.end     = Entry(container, 'End', 'mm', 70, mark="*")
        self.vel     = Entry(container, 'Velocity', 'mmps', 0.1, mark="*")
        
        self.step    = Entry(container, 'Step size', 'mm', 0.005, mark="*")
        self.wait    = Entry(container, 'Wait time', 'tcons', 1, mark="*")
        self.fast    = Option(container, 'Fast scan', [self.step, self.wait])
        
        self.sens    = Entry(container, 'Sensitivity', 'nA', 50, mark="*")
        self.tcons   = Entry(container, 'Time const.', 'ms', 100, mark="*")
        self.freq    = Entry(container, 'Frequency', 'Hz', 997)
        
        self.setup   = Entry(container, 'Setup no.', '', '')
        self.hum     = Entry(container, 'Humidity', '%', 'high')
        self.temp    = Entry(container, 'Temperature', 'K', 300)
        
        self.emit    = Entry(container, 'Emitter', '', '')
        self.vbias   = Entry(container, 'Bias voltage', 'V', 30)
        self.pumppow = Entry(container, 'Pump pow', 'mW', 10)
        
        self.detec   = Entry(container, 'Detector', '', '')
        self.probpol = Entry(container, 'Probe pol', '°', 100)
        self.probpow = Entry(container, 'Probe pow', 'mW', 10)
        
        self.pol1    = Entry(container, 'Polarizer 1', '', '')
        self.pol2    = Entry(container, 'Polarizer 2', '', '')
        self.pol3    = Entry(container, 'Polarizer 3', '', '')
        
        self.sample  = Entry(container, 'Sample', '', '')
        self.obs     = Entry(container, 'Obs.', '', '')
        self.no      = Entry(container, '#', '', '')
        
        self.smin    = Entry(container, 'Plot min', 'nA', -10, mark="*")
        self.smax    = Entry(container, 'Plot max', 'nA', 10, mark="*")
        
        self._widget_show(container)
        
        print("Parameters widget successfully created")
        
    def _widget_show(self, container):
        self.start.frame.grid(row=0, column=0, sticky=tk.W)
        self.end.frame.grid(row=1, column=0, sticky=tk.W)
        self.vel.frame.grid(row=2, column=0, sticky=tk.W)
        
        self.step.frame.grid(row=0, column=1, sticky=tk.W)
        self.wait.frame.grid(row=1, column=1, sticky=tk.W)
        self.fast.frame.grid(row=2, column=1, sticky=tk.W)
        
        self.sens.frame.grid(row=0, column=2, sticky=tk.W)
        self.tcons.frame.grid(row=1, column=2, sticky=tk.W)
        self.freq.frame.grid(row=2, column=2, sticky=tk.W)
        
        self.setup.frame.grid(row=0, column=3, sticky=tk.W)
        self.hum.frame.grid(row=1, column=3, sticky=tk.W)
        self.temp.frame.grid(row=2, column=3, sticky=tk.W)
        
        ttk.Label(container, text='').grid(row=3, column=0)  # empty row
        
        self.emit.frame.grid(row=4, column=0, sticky=tk.W)
        self.vbias.frame.grid(row=5, column=0, sticky=tk.W)
        self.pumppow.frame.grid(row=6, column=0, sticky=tk.W)
        
        self.detec.frame.grid(row=4, column=1, sticky=tk.W)
        self.probpol.frame.grid(row=5, column=1, sticky=tk.W)
        self.probpow.frame.grid(row=6, column=1, sticky=tk.W)
        
        self.pol1.frame.grid(row=4, column=2, sticky=tk.W)
        self.pol2.frame.grid(row=5, column=2, sticky=tk.W)
        self.pol3.frame.grid(row=6, column=2, sticky=tk.W)
        
        self.sample.frame.grid(row=4, column=3, sticky=tk.W)
        self.obs.frame.grid(row=5, column=3, sticky=tk.W)
        self.no.frame.grid(row=6, column=3, sticky=tk.W)
        
        ttk.Label(container, text='').grid(row=7, column=0)  # empty row
        
        self.smin.frame.grid(row=8, column=0, sticky=tk.W)
        self.smax.frame.grid(row=8, column=1, sticky=tk.W)
        
    def widget_enable(self):
        dict_ = self.__dict__
        for item in dict_.values():
            item.enable()
        print("Parameters widget enabled")
            
    def widget_disable(self):
        dict_ = self.__dict__
        for item in dict_.values():
            item.disable()
        print("Parameters widget disabled")
               
    def is_valid(self):
        try:
            b_start = isinstance(self.start.value, float)
            b_end   = isinstance(self.end.value, float)
            b_vel   = isinstance(self.vel.value, float)
            b_step  = isinstance(self.step.value, float) if not self.fast.value else True
            b_wait  = isinstance(self.wait.value, float) if not self.fast.value else True
            b_sens  = isinstance(self.sens.value, float)
            b_tcons = isinstance(self.tcons.value, float)
            b_smin  = isinstance(self.smin.value, float)
            b_smax  = isinstance(self.smax.value, float)
            srt_end = (self.start.value > self.end.value)
            return b_start and b_end and b_vel and b_step and b_wait and b_sens and b_tcons and b_smin and b_smax and srt_end
        except:
            return False

        
        
class Entry:
    def __init__(self, container, name, unit, default_value, mark=''):
        self._name  = name
        self._unit  = unit
        self._value = tk.StringVar(value=default_value)
        self._temp  = default_value
        self._lock  = False
        
        self._frame = ttk.Frame(container)
        self._label = ttk.Label(self._frame, text=f"{self._name}: {mark}", width=10)
        self._vbox  = ttk.Entry(self._frame, textvariable=self._value, justify='right', width=10)
        self._unitl = ttk.Label(self._frame, text=f"{self._unit}", width=6)
        
        options = {'sticky': tk.W, 'padx': 5, 'pady': 5}
        self._label.grid(row=0, column=0, **options)
        self._vbox.grid( row=0, column=1, **options)
        self._unitl.grid(row=0, column=2, **options)
        
    @property
    def name(self): return self._name
    @property
    def unit(self): return self._unit
    @property
    def value(self):
        try:
            return float(self._value.get())
        except:
            return self._value.get()
    @property
    def lock(self): return self._lock
    @property
    def frame(self): return self._frame
    
    def __repr__(self):
        return f"{self.name} @ {self.value}{self.unit}"
    
    def enable(self):
        if not self.lock:
            self._vbox['state'] = 'normal'
        
    def disable(self):
        if not self.lock:
            self._vbox['state'] = 'disabled'
            
    def lockit(self, value=None):
        self.disable()
        self._lock = True
        self._temp = self.value
        if value != None: self._value.set(value)
        
    def unlockit(self):
        self._lock = False
        self.enable()
        self._value.set(self._temp)
        
    def set_value(self, value):
        self._value.set(value)
        
        
        
class Option:
    def __init__(self, container, name, entries=[]):
        self._name  = name
        self._value = tk.BooleanVar()
        self._frame = ttk.Frame(container)
        
        command     = lambda: self.command(entries)
        self._check = ttk.Checkbutton(self._frame, text=f"{self._name}", variable=self._value, command=command)
        self._check.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    
    @property
    def name(self): return self._name
    @property
    def unit(self): return ''
    @property
    def value(self): return self._value.get()
    @property
    def frame(self): return self._frame
    
    def __repr__(self):
        return f"{self.name} @ {self.value}"
    
    def command(self, entries):
        if entries:
            for entry in entries:
                if self.value:
                    entry.lockit()
                else:
                    entry.unlockit()
        
    def enable(self):
        self._check['state'] = 'normal'
        
    def disable(self):
        self._check['state'] = 'disabled'
        