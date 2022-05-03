import numpy as np
import pandas as pd
from scipy.fft import fft, fftfreq


class Data:
    def __init__(self, file, dt, max_=None, pow_=None):
        self._file = file
        self._dt   = dt
        self._max  = max_
        self._pow  = pow_
        self._raw_data = self.read_file(file)
        self._time_dom = self.interp_data(self._raw_data, dt, max_=max_, pow_=pow_)
        self._freq_dom = self.compute_fft(self._time_dom, dt)

    def __repr__(self):
        return f"Data from {self.file}, cut @ t={self._max} and interpolated to 2^{self._pow} points with dt={self._dt}"

    @property
    def file(self): return self._file
    @property
    def raw(self): return self._raw_data
    @property
    def time_dom(self): return self._time_dom
    @property
    def freq_dom(self): return self._freq_dom

    @staticmethod
    def read_file(file):
        return pd.read_table(file)

    @staticmethod
    def interp_data(raw_data, dt, max_=None, pow_=None):
        dcut = raw_data.loc[raw_data['t'] <= max_] if max_ else raw_data
        tmin = min(dcut['t'])
        tmax = tmin + (dt * 2**pow_) if pow_ else max(dcut['t'])

        t = np.arange(tmin, tmax, dt)
        E = np.interp(t, dcut['t'], dcut['X'], right=0) * 1e9  # Convert A to nA
        return pd.DataFrame({'t': t, 'E': E})

    @staticmethod
    def compute_fft(data, dt):
        t = data['t'].values
        E = data['E'].values
        N = len(t)
        Efft  = np.conj(fft(E)[:N//2])
        ampl  = (2/N) * np.abs(Efft)
        phase = np.angle(Efft)
        freq  = fftfreq(N, dt)[:N//2]
        return pd.DataFrame({'freq': freq, 'ampl': ampl, 'phase': phase, 'fft': Efft})
    
    