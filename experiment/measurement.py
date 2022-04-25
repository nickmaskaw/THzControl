import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
import os
import time as tm



class Constants:
    C = 299_792_458e3/1e12  # mm/ps (~0.3mm/ps)



class Convert:
    @staticmethod
    def ps_to_mm(t):
        return t * Constants.C
    @staticmethod
    def mm_to_ps(d):
        return d / Constants.C
    @staticmethod
    def raw_to_sig(multimeter_read, sensitivity):
        raw_fullscale = 10  # V
        return multimeter_read * (sensitivity / raw_fullscale)
    @staticmethod
    def sig_to_raw(signal, sensitivity):
        raw_fullscale = 10  # V
        return signal * (raw_fullscale / sensitivity)



class Measurement:
    DATA_FOLDER = './output/data'
    CONF_FOLDER = './output/config'
    PLOT_FOLDER = './output/plot'
    
    def __init__(self, container, multimeter, delay_line, prefs):
        self._check_output_folder()
        self._create_widget(container)
        
        self._multimeter = multimeter
        self._delay_line = delay_line
        self._prefs      = prefs
        
    def _check_output_folder(self):
        folders = [Measurement.DATA_FOLDER, Measurement.CONF_FOLDER, Measurement.PLOT_FOLDER]
        for folder in folders:
            if not os.path.exists(folder): os.makedirs(folder)
        print("Checked measurement output folders")
        
    def _create_widget(self, container):        
        self._set_button   = ttk.Button(container, text="Set", command=self._set_command)
        self._start_button = ttk.Button(container, text="Start", command=self._start_command, state='disabled')
        self._text         = ttk.Label(container, text="")
        
        options = {'sticky': tk.W, 'padx': 5, 'pady': 5}
        self._set_button.grid(row=0, column=0, **options)
        self._start_button.grid(row=0, column=1, **options)
        self._text.grid(row=0, column=2, **options)
        
        print("Measurement widget successfully created")
        
    def _set_command(self):
        if self._set_button['text'] == "Set":
            if not self._multimeter.is_connected():
                self._text['text'] = "ERROR: Multimeter is not connected!"
            elif not self._delay_line.is_connected():
                self._text['text'] = "ERROR: Delay line is not connected!"
            elif not self._prefs.is_valid():
                self._text['text'] = "ERROR: Invalid value for required (*) items!" 
            else:
                self._set()   
        elif self._set_button['text'] == "Unset":
            self._unset()
                  
    def _set(self):
        try:
            self._delay_line.return_to(self._prefs.start.value)
            self._delay_line._button_get()
            self._text['text']          = "Set"
            self._set_button['text']    = "Unset"
            self._start_button['state'] = 'normal'
            self._multimeter.widget_disable()
            self._delay_line.widget_disable()
            self._prefs.widget_disable()
            self._prefs.save_preset()
        except:
            self._text['text'] = "ERROR: Could not set the delay line to start position."
            
    def _unset(self):
        if self._text['text'] == "Set": self._text['text'] = ""
        self._set_button['text']    = "Set"
        self._start_button['state'] = 'disabled'
        self._multimeter.widget_enable()
        self._delay_line.widget_enable()
        self._prefs.widget_enable()
            
    def _start_command(self):
        self._start_button['state'] = 'disabled'
        self._set_button['state'] = 'disabled'
        self._start()
        self._unset()
        self._set_button['state'] = 'normal'
        
    def _dataframe(self, x, dx, y):
        t = Convert.mm_to_ps(2 * (x[0] - x))
        return DataFrame({'t': t, 'y': y, 'x': x, 'dx': dx})
    
    def _filename(self):
        timestamp = tm.strftime('%Y%m%d-%H%M%S')
        fast      = "fastscan" if self._prefs.fast.value else "stepscan"
        setup     = self._prefs.setup.value
        sample    = self._prefs.sample.value
        obs       = self._prefs.obs.value
        no        = self._prefs.no.value 
        return f"{timestamp}_{fast}_{setup}_{sample}_{obs}_{no}"
    
    def _save(self, data, fig):
        filename = self._filename()
        self._prefs.save(Measurement.CONF_FOLDER, filename)
        data.to_csv(f'{Measurement.DATA_FOLDER}/{filename}.dat', sep='\t', index=False)
        fig.savefig(f'{Measurement.PLOT_FOLDER}/{filename}.png', dpi=72)
        self._text['text'] = f"Saved as {filename}"
    
    def _start(self):
        start = self._prefs.start.value
        end   = self._prefs.end.value
        vel   = self._prefs.vel.value
        step  = self._prefs.step.value
        wait  = self._prefs.wait.value
        fast  = self._prefs.fast.value
        tcons = self._prefs.tcons.value * 1e-3  # time constant in seconds
        sens  = self._prefs.sens.value
        
        ymin  = Convert.sig_to_raw(self._prefs.smin.value, sens)
        ymax  = Convert.sig_to_raw(self._prefs.smax.value, sens)
        
        plot = LivePlot(start, end, ymin, ymax)
        
        self._delay_line.start_polling(10)
        self._delay_line.set_vel(vel)
        
        # CONTINUOUS MEASUREMENTS ############################################
        if fast:
            dt  = 0.1
            t0  = tm.time()
            T   = (start - end) / vel
            N   = int(T / dt)
            
            v   = np.full(N, np.nan)  # Multimeter reads
            d   = np.full(N, np.nan)  # Delay line positions
            
            self._delay_line.move_to(end, timeout=0)
            for i in range(N):
                tm.sleep(dt - (tm.time() - t0) % dt)
                
                d[i] = self._delay_line.get_pos()
                v[i] = self._multimeter.get_meas()
                plot.update(d, v)
                
                if d[i] <= end: break
            
            x, dx = d, np.full(N, np.nan)
            y     = Convert.raw_to_sig(v, sens)
           
        # STEP MEASUREMENTS ##################################################
        else:
            pos = np.arange(start, end, -step)
            N   = len(pos)
            
            v   = np.full(N, np.nan)  # Multimeter reads
            d   = np.full(N, np.nan)  # Delay line positions
            
            for i in range(N):
                self._delay_line.move_to(pos[i])
                tm.sleep(wait * tcons)
                
                d[i] = self._delay_line.get_pos()
                v[i] = self._multimeter.get_meas()
                plot.update(d, v)
                
            x, dx = pos, (d - pos)
            y     = Convert.raw_to_sig(v, sens)
            
        ######################################################################
        self._delay_line.stop_polling()
        plot.final(x, y)
        plt.tight_layout()
        
        data = self._dataframe(x, dx, y)
        fig  = plot.fig
        self._save(data, fig)
            
    
    
class LivePlot:
    def __init__(self, start, end, ymin, ymax):
        self._start = start
        self._end   = end
        self._ymin  = ymin
        self._ymax  = ymax
        
        self._create()
    
    def _create(self):
        plt.close('all')
        self._fig   = plt.figure('live_plot', figsize=[9, 7])
        self._ax    = self._fig.add_subplot(111)
        self._line, = self._ax.plot(np.nan, np.nan)
        plt.show(block=False)
        self._fig.canvas.draw()
        self._ax.set_xlim([self._start, self._end])
        self._ax.set_ylim([self._ymin, self._ymax])
        
    def update(self, x_data, y_data):
        self._line.set_xdata(x_data)
        self._line.set_ydata(y_data)
        self._ax.draw_artist(self._ax.patch)
        self._ax.draw_artist(self._line)
        self._fig.canvas.update()
        self._fig.canvas.flush_events()
        
    def final(self, x_data, y_data):
        plt.close('all')
        self._fig = plt.figure('final plot', figsize=[9, 7])
        self._ax  = self._fig.add_subplot(111)
        self._ax.plot(x_data, y_data)
        self._ax.set_xlim([self._start, self._end])
        self._fig.show()
        
    @property
    def fig(self): return self._fig