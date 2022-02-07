class Attribute:
    def __init__(self, name, data_type, init_value, cb_value_change=None):
        self.name = name
        self.type = data_type
        self.init_value = init_value
        self.value = init_value
        self.comm_obj = None
        self.cb_value_change = cb_value_change

    def set_value(self, value):
        if not self.validate_type(value):
            return False
        self.value = value

        if self.cb_value_change is not None:
            self.cb_value_change(value)

        if self.comm_obj is not None:
            if self.comm_obj.write_value_callback is not None:
                self.comm_obj.write_value_callback(value)
        return True

    def validate_type(self, value):
        return type(value) == self.type

    def attach_communication_object(self, communication_object):
        self.comm_obj = communication_object
