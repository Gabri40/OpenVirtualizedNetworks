from node import *

class Line(object):
    def __init__(self, line_dict):
        self._label = line_dict['label']
        self._length = line_dict['length']
        self._successive = {}
        self._state=["free"]*10
    
    @property
    def label(self):
        return self._label
    
    @property
    def length(self):
        return self._length
    
    @property
    def successive(self):
        return self._successive
    @successive.setter
    def successive(self, successive):
        self._successive = successive

    @property 
    def state(self): 
        return self._state
    @state.setter
    def state(self,state): 
        self._state=state
    
    def latency_generation(self):
        latency = self.length /(3e8 * 2 / 3)
        return latency
    
    def noise_generation(self, signal_power):
        noise=1e-9*signal_power*self.length
        return noise
    
    def propagate(self, signal_information,busy=False):
        # Update latency
        latency = self.latency_generation()
        signal_information.add_latency(latency)

        # Update noise
        signal_power = signal_information.signal_power
        noise = self.noise_generation(signal_power)
        signal_information.add_noise(noise)

        # print("prop: "+str(self.label))
        node = self.successive[signal_information.path[0]]
        signal_information = node.propagate(signal_information,busy)
        return signal_information