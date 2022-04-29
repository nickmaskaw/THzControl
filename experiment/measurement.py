import os
import time as tm
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from experiment import LivePlot


class Constants:
    C = 299_792_458e3/1e12  # mm/ps (~0.3mm/ps)


class Convert:
    @staticmethod
    def ps_to_mm(t):
        return t * Constants.C

    @staticmethod
    def mm_to_ps(d):
        return d / Constants.C


class Measurement:
    DATA_FOLDER = './output/data'
    INFO_FOLDER = './output/info'
    PLOT_FOLDER = './output/plot'

    def __init__(self, parameters, lock_in, thermometer, delay_line):
        self._parameters  = parameters
        self._lock_in     = lock_in
        self._thermometer = thermometer
        self._delay_line  = delay_line
        self._widget      = None

        self._check_output_folder()

    @property
    def parameters(self): return self._parameters
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
        self._widget = MeasurementWidget(frame, self)
        print("Measurement widget successfully created")
        
    def start(self):
        start = float(self.parameters.user.start.value)
        end   = float(self.parameters.user.end.value)
        vel   = float(self.parameters.user.vel.value)
        step  = float(self.parameters.user.step.value)
        wait  = float(self.parameters.user.wait.value)
        fast  = self.parameters.user.fast.value
        tcons = float(self.parameters.hidden.tcons.value)
        ymax  = float(self.parameters.user.ymax.value) * 1e-9  # convert to A
        
        plot  = LivePlot(start, end, -ymax, ymax)
        
        self.delay_line.return_to(start)
        self.delay_line.start_polling(10)
        self.delay_line.set_vel(vel)
        
        # Continuous measurements #############################################
        if fast:
            dt = .1
            t0 = tm.time()
            T  = (start - end) / vel
            N  = int(T / dt)
            
            d = np.full(N, np.nan)  # Delay line positions
            X = np.full(N, np.nan)  # Lock-in X measurement
            Y = np.full(N, np.nan)  # Lock-in Y measurement
            R = np.full(N, np.nan)  # Thermometer resistance
            
            self.delay_line.move_to(end, timeout=0)
            for i in range(N):
                tm.sleep(dt - (tm.time() - t0) % dt)
                
                d[i]       = self.delay_line.get_pos()
                X[i], Y[i] = self.lock_in.get_XY()
                R[i]       = self.thermometer.get_fres()
                
                plot.update(d, X)
                if d[i] <= end: break
            
            pos, dpos = d, np.full(N, np.nan)

        # Step measurements ###################################################
        else:
            pos = np.arange(start, end, -step)
            N   = len(pos)
            
            d = np.full(N, np.nan)  # Delay line positions
            X = np.full(N, np.nan)  # Lock-in X measurement
            Y = np.full(N, np.nan)  # Lock-in Y measurement
            R = np.full(N, np.nan)  # Thermometer resistance
            
            for i in range(N):
                self._delay_line.move_to(pos[i])
                tm.sleep(wait * tcons)
                
                d[i]       = self.delay_line.get_pos()
                X[i], Y[i] = self.lock_in.get_XY()
                R[i]       = self.thermometer.get_fres()
                
                plot.update(d, X)
                
            dpos  = (d - pos)
        
        #######################################################################
        self.delay_line.stop_polling()
        plot.final(pos, X)
        
        data = self._dataframe(pos, dpos, X, Y, R)
        fig  = plot.fig
        self._save(data, fig)

    def _save(self, data, fig):
        filename = self._filename()
        
        self.parameters.save(self.INFO_FOLDER, f'{filename}.txt')
        data.to_csv(f'{self.DATA_FOLDER}/{filename}.dat', sep='\t', index=False)
        fig.savefig(f'{self.PLOT_FOLDER}/{filename}.png', dpi=72)
        
        message = f"Saved data as {filename}"
        self.widget.set_message(message)
        print(message)

    @staticmethod
    def _dataframe(pos, dpos, X, Y, R):
        t = Convert.mm_to_ps(2 * (pos[0] - pos))
        return pd.DataFrame({'t': t, 'X': X, 'Y': Y, 'R': R, 'pos': pos, 'dpos': dpos})
    
    def _filename(self):
        timestamp = tm.strftime('%Y%m%d-%H%M%S')
        start     = self.parameters.user.start.value
        end       = self.parameters.user.end.value
        fast      = "fastscan" if self.parameters.user.fast.value else "steppedscan"
        setup     = self.parameters.label.setup.value
        sample    = self.parameters.label.sample.value
        obs       = self.parameters.label.obs.value
        return f"{timestamp}_{start}to{end}mm_{fast}_{setup}_{sample}_{obs}"


class MeasurementWidget:
    def __init__(self, frame, measurement):
        self._measurement  = measurement
        self._start_button = ttk.Button(frame, text="Start", command=self._start)
        self._message      = ttk.Label(frame, text="")

        options = {'sticky': tk.W, 'padx': 5, 'pady': 5}
        self._start_button.grid(row=0, column=1, **options)
        self._message.grid(row=0, column=2, **options)
        
    @property
    def measurement(self): return self._measurement
    
    @property
    def _all_set(self):
        set_params = self.measurement.parameters.widget.is_set
        set_lockin = self.measurement.lock_in.is_connected
        set_thermo = self.measurement.thermometer.is_connected
        set_delayl = self.measurement.delay_line.is_connected
        
        return set_params and set_lockin and set_thermo and set_delayl

    def set_message(self, message):
        self._message['text'] = message

    def _start(self):
        if self._all_set:
            print("Measurement start")
            self.measurement.start()
            self.measurement.parameters.widget.unset()
