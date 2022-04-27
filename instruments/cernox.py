from instruments import Multimeter


class Cernox(Multimeter):
    def __init__(self, name="Cernox"):
        super().__init__(name)

    # Try to implement some sort of temperature conversion...
