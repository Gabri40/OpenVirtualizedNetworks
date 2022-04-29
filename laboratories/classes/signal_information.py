class SignalInformation:

    def __init__(self, signal_power):
        self.signal_power = signal_power
        self.path = {}  # list[string]
        self.noise_power = 0.0
        self.latency = 0.0
        self.path_index = 0  # index in path where signal currently is

    # update values , increment
    def add_power(self, value):
        self.signal_power += value

    def add_noise(self, value):
        self.noise_power += value

    def add_latency(self, value):
        self.latency += value

    # update path
    def update_path(self):
        self.path_index += 1

    def extend_path(self, node):
        self.path.append(node)

    # get self
    def get_signal_info(self):
        return self

    # power
    def get_sig_power(self):
        return self.signal_power

    def set_sig_power(self, power):
        self.signal_power = power

    # path, list of letters
    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path

    # latency
    def get_latency(self):
        return self.latency

    def set_latency(self, lat):
        self.latency = lat

    # noise
    def get_noise_power(self):
        return self.noise_power

    def set_noise_power(self, noise):
        self.noise_power = noise
