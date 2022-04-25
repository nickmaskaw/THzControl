import numpy as np
import pandas as pd
from scipy.fft import fft, fftfreq

class Data:
    def __init__(self, file, dt, time_range=(None, None), delayline_zero=None):
        self._raw_data = self._read_file(file)
        self._time_dom = self._interp_data(self._raw_data, dt)
        self._freq_dom = self._compute_fft(self._time_dom, dt)
        
    @property
    def time_dom(self): return self._time_dom
    @property
    def freq_dom(self): return self._freq_dom
    
    def _read_file(self, file):
        return pd.read_table(file)
    
    def _interp_data(self, raw_data, dt):
        t = np.arange(min(raw_data['t'].values), max(raw_data['t'].values), dt)
        y = np.interp(t, raw_data['t'].values, raw_data['y'].values)
        return pd.DataFrame({'t': t, 'y': y})
    
    def _compute_fft(self, data, dt):
        t = data['t'].values
        y = data['y'].values
        N = len(t)
        yt    = np.conj(fft(y)[:N//2])
        ampl  = (2/N) * np.abs(yt)
        phase = np.angle(yt)
        freq  = fftfreq(N, dt)[:N//2]
        return pd.DataFrame({'freq': freq, 'ampl': ampl, 'phase': phase, 'fft': yt})
    
    