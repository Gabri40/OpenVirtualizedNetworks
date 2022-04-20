class Line:

    def __init__(self, label, pos1, pos2):
        self.label = label
        self.lenght = (pos1[0] - pos2[0], pos1[1] - pos2[1])
        self.successive = {}  # nodes dict

    # latency gen, assuminc c=3*10^8m/s

    # label
    def get_label(self): return self.label

    def set_label(self, lab): self.label = lab

    # lenght
    def get_lenght(self): return self.lenght

    def set_lenght(self, l): self.lenght = l

    # successive
    def get_successive(self): return self.successive

    def set_successive(self, successive_dic): self.successive = successive_dic
