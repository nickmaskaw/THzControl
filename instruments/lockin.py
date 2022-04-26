from instruments import VISAInstrument


class Lockin(VISAInstrument):
    # first col: values in nA (or mV); second col: lock-in parameters
    SENS_LIST = {
        1:    17,
        2:    18,
        5:    19,
        10:   20,
        20:   21,
        50:   22,
        100:  23,
        200:  24,
        500:  25,
        1000: 26
    }

    # first col: values in ms; second col: lock-in parameters
    TCONS_LIST = {
        1:    4,
        3:    5,
        10:   6,
        30:   7,
        100:  8,
        300:  9,
        1000: 10
    }

    def __init__(self):
        super().__init__(name="Lock-in")

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

    def set_sens(self, i):
        self.instr.write(f'SENS {i}')

    def set_tcons(self, i):
        self.instr.write(f'OFLT {i}')