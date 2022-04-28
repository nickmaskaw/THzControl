import os
import tkinter as tk
from tkinter import ttk


class MeasurementControl:
    DATA_FOLDER = './output/data'
    INFO_FOLDER = './output/info'
    PLOT_FOLDER = './output/plot'

    def __init__(self, lock_in, thermometer, delay_line):
        self._lock_in     = lock_in
        self._thermometer = thermometer
        self._delay_line  = delay_line

    def _check_output_folder(self):
        folders = [self.DATA_FOLDER, self.INFO_FOLDER, self.PLOT_FOLDER]
        for folder in folders:
            if not os.path.exists(folder): os.makedirs(folder)
        print("Checked measurement output folders")


class MeasurementWidget:
    def __init__(self, frame):
        self._set_button   = ttk.Button(frame, text="Set", command=self._set_command)
        self._start_button = ttk.Button(frame, text="Start", command=self._start_command)
        self._status       = ttk.Label(frame, text="")

        options = {'sticky': tk.W, 'padx': 5, 'pady': 5}
        self._set_button.grid(row=0, column=0, **options)
        self._start_button.grid(row=0, column=1, **options)
        self._text.grid(row=0, column=2, **options)

    def _set_command(self):
        pass

    def _start_command(self):
        pass
