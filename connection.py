class Connection(object):

    def __init__(self, inp, outp, pw):
        self._input_node = inp  # node, start
        self._ouput_node = outp  # node, end
        self._signal_power = pw
        self._latency = 0.0
        self._snr = 0.0

    # nodes
    def input_node(self):
        return self._input_node

    def output_node(self):
        return self._ouput_node

    # power
    def signal_power(self):
        return self._signal_power

    # latency
    def latency(self):
        return self._latency

    def set_latency(self,val):
        self._latency=val

    # snr
    def snr(self):
        return self._snr

    def set_snr(self, value):
        self._snr = value
