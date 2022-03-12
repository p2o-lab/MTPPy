class CommandCodes:
    def __init__(self):
        self.reset = 2
        self.start = 4
        self.stop = 8
        self.hold = 16
        self.unhold = 32
        self.pause = 64
        self.resume = 128
        self.abort = 256
        self.restart = 512
        self.complete = 1024

        self.int_code = {}
        self.int_code[2] = 'reset'
        self.int_code[4] = 'start'
        self.int_code[8] = 'stop'
        self.int_code[16] = 'hold'
        self.int_code[32] = 'unhold'
        self.int_code[64] = 'pause'
        self.int_code[128] = 'resume'
        self.int_code[256] = 'abort'
        self.int_code[512] = 'restart'
        self.int_code[1024] = 'complete'

    def get_list_int(self):
        return list(self.int_code.keys())

    def get_list_str(self):
        return list(self.int_code.values())
