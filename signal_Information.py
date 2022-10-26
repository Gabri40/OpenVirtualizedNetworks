class SignalInformation(object):

    def __init__(self, power, path):
        self._signal_power = power
        self._path = path
        self._noise_power = 0.0
        self._latency = 0.0

    # power
    def signal_power(self):
        return self._signal_power

    # path
    def path(self):
        return self._path

    def set_path(self, path):
        self._path = path

    # noise
    def noise_power(self):
        return self._noise_power

    def set_noise_power(self, noise):
        self._noise_power = noise

    def add_noise(self, amount):
        self._noise_power += amount

    # latency
    def latency(self):
        return self._latency

    def set_latency(self, lat):
        self._latency = lat

    def add_latency(self, amount):
        self._latency += amount

    # path movement
    def next_node(self):
        self._path = self._path[1:]  # "pop" first elem in path list ,