import matplotlib.pyplot as plt
import numpy as np


class LivePlot:
    def __init__(self, start, end, ymin, ymax):
        self._start = start
        self._end   = end
        self._ymin  = ymin
        self._ymax  = ymax
        self._fig   = None
        self._ax    = None
        self._line  = None
        self._create()

    @property
    def fig(self): return self._fig

    def _create(self):
        plt.close('all')
        self._fig   = plt.figure('live_plot', figsize=[9, 7])
        self._ax    = self._fig.add_subplot(111)
        self._line, = self._ax.plot(np.nan, np.nan)
        plt.show(block=False)
        self._fig.canvas.draw()
        self._ax.set_xlim([self._start, self._end])
        self._ax.set_ylim([self._ymin, self._ymax])
        plt.tight_layout()

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
        self._ax = self._fig.add_subplot(111)
        self._ax.plot(x_data, y_data)
        self._ax.set_xlim([self._start, self._end])
        self._fig.show()
        plt.tight_layout()
