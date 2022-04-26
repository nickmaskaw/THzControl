from instruments import VISAInstrument


class Multimeter(VISAInstrument):
    def __init__(self, name="Multimeter"):
        super().__init__(name)

    def get_volt(self):
        volt = self.instr.query('MEAS?')
        return float(volt)

    def get_curr(self):
        curr = self.instr.query('MEAS:CURR?')
        return float(curr)

    def get_fres(self):
        fres = self.instr.query('MEAS:FRES?')
        return float(fres)

    def get_res(self):
        res = self.instr.query('MEAS:RES?')
        return float(res)