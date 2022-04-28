import os
import tkinter as tk
from tkinter import ttk


class Measurement:
    DATA_FOLDER = './output/data'
    INFO_FOLDER = './output/info'
    PLOT_FOLDER = './output/plot'

    def __init__(self, lock_in, thermometer, delay_line):
        self._lock_in     = lock_in
        self._thermometer = thermometer
        self._delay_line  = delay_line
        self._widget      = None

        self._check_output_folder()

    @property
    def lock_in(self): return self._lock_in
    @property
    def thermometer(self): return self._thermometer
    @property
    def delay_line(self): return self._delay_line
    @property
    def widget(self): return self._widget

    def _check_output_folder(self):
        folders = [self.DATA_FOLDER, self.INFO_FOLDER, self.PLOT_FOLDER]
        for folder in folders:
            if not os.path.exists(folder): os.makedirs(folder)
        print("Checked measurement output folders")

    def create_widget(self, frame):
        self._widget = MeasurementWidget(frame)
        print("Measurement widget successfully created")


class MeasurementWidget:
    def __init__(self, frame):
        self._start_button = ttk.Button(frame, text="Start", command=self._start)
        self._status       = ttk.Label(frame, text="")

        options = {'sticky': tk.W, 'padx': 5, 'pady': 5}
        self._start_button.grid(row=0, column=1, **options)
        self._status.grid(row=0, column=2, **options)

    def _start(self):
        print("Measurement start")
