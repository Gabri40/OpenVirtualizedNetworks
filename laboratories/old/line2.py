import math


class Line:

    def __init__(self, label, pos1, pos2):
        self.label = label
        self.start = pos1
        self.end = pos2
        self.lenght = math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
        self.successive = {}  # nodes dict
        # self.state = 1  # values 1-free or 0-occupied  : shows if a connection is occupying the line
        self.state = ["free"] * 10

    # state
    def occupy_line_channel(self, chan):
        self.state[chan] = "busy"

    def free_line_chanmel(self, chan):
        self.state[chan] = "free"

    def is_channel_free(self, chan):
        if self.state[chan] == "free":
            return True
        else:
            return False

    # latency gen, assuminc c=3*10^8m/s
    def latency_generation(self):
        return self.lenght / 3e8

    def noise_generation(self, signal_power):
        return 1e-9 * signal_power * self.lenght

    # label
    def get_label(self):
        return self.label

    def set_label(self, lab):
        self.label = lab

    # lenght
    def get_lenght(self):
        return self.lenght

    def set_lenght(self, l):
        self.lenght = l

    # successive
    def get_successive(self):
        return self.successive

    def add_successive(self, succ):
        self.successive[succ.get_label()] = succ

    # start finish
    def get_start(self):
        return self.start

    def get_end(self):
        return self.end
