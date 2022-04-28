import pandas as pd
import tkinter as tk
from tkinter import ttk


class Parameters:
    PRESET_FOLDER = './preset'
    PRESET_FILE   = 'preferences'

    def __init__(self):
        self._user   = UserParams()
        self._label = LabelParams()
        self._hidden = HiddenParams()
        self._widget = None

        self._load_preset()

    @property
    def user(self): return self._user
    @property
    def label(self): return self._label
    @property
    def hidden(self): return self._hidden
    @property
    def widget(self): return self._widget

    @property
    def table(self):
        table_ = pd.concat([self.user.table, self.label.table, self.hidden.table])
        return table_

    def create_widget(self, frame):
        self._widget = ParametersWidget(frame, self)
        print(f"Parameters widget successfully created")

    def save(self, folder, file):
        self.table.to_csv(f'{self.PRESET_FOLDER}/{self.PRESET_FILE}', sep='\t')
        print(f"Saved parameters to {self.PRESET_FOLDER}/{self.PRESET_FILE}")

    def _load_preset(self):
        self.user.load(self.PRESET_FOLDER, self.PRESET_FILE)
        self.label.load(self.PRESET_FOLDER, self.PRESET_FILE)
        print("Loaded preset parameters")


class ParametersWidget:
    def __init__(self, frame, parameters):
        self._parameters = parameters

        user_width    = 10
        label_width_1 = 10
        label_width_2 = 40

        for i, key in enumerate(parameters.user.dic):
            if key not in ['fast']:
                self.__dict__[key] = Entry(frame, parameters.user.dic[key], user_width)
            else:
                self.__dict__[key] = CheckButton(frame, parameters.user.dic[key])
            self.__dict__[key].container.grid(row=i, column=0, sticky=tk.W)

        for i, key in enumerate(parameters.label.dic):
            special_keys = ['pols', 'sample', 'obs']
            label_width  = label_width_2 if key in special_keys else label_width_1
            column       = 2 if key in special_keys else 1
            row          = i-5 if key in special_keys else i
            self.__dict__[key] = Entry(frame, parameters.label.dic[key], label_width)
            self.__dict__[key].container.grid(row=row, column=column, sticky=tk.W)

        self.setbtn = ttk.Button(frame, text="Set parameters", command=self._setbtn_clicked)
        self.setbtn.grid(row=4, column=2, sticky=tk.W)

    def _set_parameters(self):
        for key in self._parameters.user.dic:
            self.__dict__[key].to_param()
        for key in self._parameters.label.dic:
            self.__dict__[key].to_param()
        print("Parameters are set")

    def _setbtn_clicked(self):
        self._set_parameters()
        self._parameters.save(self._parameters.PRESET_FOLDER, self._parameters.PRESET_FILE)


class Param:
    def __init__(self, name, unit=''):
        self._name  = name
        self._unit  = unit
        self._value = ''

    def __repr__(self):
        return f"Parameter {self.name} @ {self.value}{self.unit}"

    @property
    def name(self): return self._name
    @property
    def unit(self): return self._unit
    @property
    def value(self): return self._value

    @property
    def table(self):
        dict_ = {'name': self.name, 'unit': self.unit, 'value': self.value}
        return pd.DataFrame(dict_, index=[0])

    def set_value(self, value):
        self._value = value


class ParamSet:
    @property
    def dic(self): return self.__dict__

    @property
    def table(self):
        table_ = pd.DataFrame()
        for param in self.dic:
            df = self.dic[param].table
            df.index = [param]
            table_ = table_.append(df)
        return table_

    def load(self, folder, file):
        df = pd.read_table(f'{folder}/{file}', index_col=0).fillna('')
        for param in self.dic:
            if param in df.index:
                self.dic[param].set_value(df['value'][param])


class UserParams(ParamSet):
    def __init__(self):
        self.start = Param('Start', 'mm')
        self.end   = Param('End', 'mm')
        self.vel   = Param('Velocity', 'mmps')
        self.step  = Param('Step size', 'mm')
        self.wait  = Param('Wait time', 'tcons')
        self.fast  = Param('Fast scan')


class LabelParams(ParamSet):
    def __init__(self):
        self.setup  = Param('Setup no.')
        self.hum    = Param('Humidity', '%')
        self.temp   = Param('Temperature', 'K')
        self.emit   = Param('Emmiter')
        self.detec  = Param('Detector')
        self.pols   = Param('Polarizers')
        self.sample = Param('Sample')
        self.obs    = Param('Obs')


class HiddenParams(ParamSet):
    def __init__(self):
        self.sens  = Param('Sensitivity', 'nA')
        self.tcons = Param('Time const.', 's')
        self.freq  = Param('Chop freq', 'Hz')


class Entry:
    def __init__(self, frame, param, width):
        self._param      = param
        self._entryvalue = tk.StringVar(value=self._param.value)
        self._container  = ttk.Frame(frame)

        self._label     = ttk.Label(self._container, text=f"{self._param.name}:", width=10)
        self._valuebox  = ttk.Entry(self._container, textvariable=self._entryvalue, justify='right', width=width)
        self._unitlabel = ttk.Label(self._container, text=self._param.unit, width=6)

        options = {'sticky': tk.W, 'padx': 5, 'pady': 5}
        self._label.grid(row=0, column=0, **options)
        self._valuebox.grid(row=0, column=1, **options)
        self._unitlabel.grid(row=0, column=2, **options)

    @property
    def container(self): return self._container
    @property
    def value(self): return self._entryvalue.get()

    def to_param(self):
        self._param.set_value(self.value)


class CheckButton:
    def __init__(self, frame, param):
        self._param     = param
        self._var       = tk.BooleanVar()
        self._container = ttk.Frame(frame)

        self._checkbtn = ttk.Checkbutton(self._container, text=self._param.name, variable=self._var)
        self._checkbtn.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

    @property
    def container(self): return self._container
    @property
    def value(self): return self._var.get()

    def to_param(self):
        self._param.set_value(self.value)
