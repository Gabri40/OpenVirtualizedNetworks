class Line:

    def __init__(self, label, pos1, pos2):
        self.label = label
        self.start = pos1
        self.end = pos2
        self.lenght = (pos1[0] - pos2[0], pos1[1] - pos2[1]) # ???????????????????????????????????
        self.successive = {}  # nodes dict

    # latency gen, assuminc c=3*10^8m/s
    def latency_generation(self):
        return self.lenght / 3e8

    def noise_generation(self, signal_power):
        return 1e-9 * signal_power * self.length

    # label
    def get_label(self): return self.label

    def set_label(self, lab): self.label = lab

    # lenght
    def get_lenght(self): return self.lenght

    def set_lenght(self, l): self.lenght = l

    # successive
    def get_successive(self): return self.successive

    def add_successive(self, succ): self.successive[succ.get_label()] = succ

    # start finish
    def get_start(self): return self.start

    def get_end(self): return self.end
