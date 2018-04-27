class ThermalCycleRule:
    """
        Thermal cycle rule are specific to a entire plate ,
        They contain instructions as temperature steps and number of repeat
        cycles
        Note : they contain a unit field which is always 'x'
    """

    def __init__(self, temperature_steps, cycle,unit):
        self.temperature_steps = temperature_steps
        self.cycles = cycle
        self.units = unit

    def todict(self):
        return self.__dict__