from instruments import VISAInstrument


class Lockin(VISAInstrument):
    # first col: lock-in index; second col: values in nA (or mV)
    SENS_LIST = {
        '17': 1,
        '18': 2,
        '19': 5,
        '20': 10,
        '21': 20,
        '22': 50,
        '23': 100,
        '24': 200,
        '25': 500,
        '26': 1000
    }

    # first col: lock-in index; second col: values in s
    TCONS_LIST = {
        '0':  10e-6,
        '1':  30e-6,
        '2':  100e-6,
        '3':  300e-6,
        '4':  1e-3,
        '5':  3e-3,
        '6':  10e-3,
        '7':  30e-3,
        '8':  100e-3,
        '9':  300e-3,
        '10': 1,
        '11': 3,
        '12': 10,
        '13': 30,
        '14': 100,
        '15': 300,
        '16': 1e3,
        '17': 3e3,
        '18': 10e3,
        '19': 30e3
    }

    def __init__(self, name="Lock-in"):
        super().__init__(name)

    def get_XY(self):
        X, Y = self.instr.query('SNAP?1,2').split(',')
        return float(X), float(Y)

    def get_X(self):
        X = self.instr.query('OUTP?1')
        return float(X)

    def get_Y(self):
        Y = self.instr.query('OUTP?2')
        return float(Y)

    def get_phase(self):
        phase = self.instr.query('PHAS?')
        return float(phase)

    def get_freq(self):
        freq = self.instr.query('FREQ?')
        return float(freq)

    def get_sens(self):
        i = self.instr.query('SENS?')
        return self.SENS_LIST[i]

    def get_tcons(self):
        i = self.instr.query('OFLT?')
        return self.TCONS_LIST[i]
    