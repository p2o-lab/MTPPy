class StateCodes:
    def __init__(self):
        #self.undefined = 1
        self.stopped = 4
        self.starting = 8
        self.idle = 16
        self.paused = 32
        self.execute = 64
        self.stopping = 128
        self.aborting = 256
        self.aborted = 512
        self.holding = 1024
        self.held = 2048
        self.unholding = 4096
        self.pausing = 8192
        self.resuming = 16384
        self.resetting = 32678
        self.completing = 65536
        self.completed = 131072

        self.int_code = {}
        #self.int_code[1] ='undefined'
        self.int_code[4] = 'stopped'
        self.int_code[8] = 'starting'
        self.int_code[16] = 'idle'
        self.int_code[32] = 'paused'
        self.int_code[64] = 'execute'
        self.int_code[128] = 'stopping'
        self.int_code[256] = 'aborting'
        self.int_code[512] = 'aborted'
        self.int_code[1024] = 'holding'
        self.int_code[2048] = 'held'
        self.int_code[4096] = 'unholding'
        self.int_code[8192] = 'pausing'
        self.int_code[16384] = 'resuming'
        self.int_code[32678] = 'resetting'
        self.int_code[65536] = 'completing'
        self.int_code[131072] = 'completed'

    def get_list_int(self):
        return list(self.int_code.keys())

    def get_list_str(self):
        return list(self.int_code.values())
