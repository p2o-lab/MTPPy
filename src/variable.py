class Variable:
    def __init__(self, name, init_value, opcua_node_obj, opcua_type, writable=True, callback=None):
        self.name = name
        self.init_value = init_value
        self.value = init_value
        self.opcua_node_obj = opcua_node_obj
        self.callback = callback
        self.writable = writable
        self.opcua_type = opcua_type

    def read_value(self):
        self.value = self.opcua_node_obj.get_value()

    def write_value(self, value):
        self.value = value
        self.opcua_node_obj.set_value(value)

    def return_value(self):
        return self.value
