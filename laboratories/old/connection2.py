class Connection:
    def __init__(self, inp, outp, pw):
        self.input = inp  # node, start
        self.output = outp  # node, end
        self.signal_power = pw
        self.latency = 0.0
        self.snr = 0.0
        self.available = True

    # Moreover,
    # modify the stream network method such that, if there are not any avail-
    # able path between the input and the output nodes of a connection, the
    # resulting snr and latency have to be set to zero and ’None’, respectively.
    #
    # i use a boolean value to determine is path is available instead
    def is_path_available(self): return self.available

    def set_availability(self, boolean): self.available = boolean

    def get_input_node(self): return self.input

    def get_output_node(self): return self.output

    def get_signal_power(self): return self.signal_power

    def get_latency(self): return self.latency

    def set_latency(self, lat): self.latency = lat

    def get_snr(self): return self.snr

    def set_snr(self, snr): self.snr = snr
