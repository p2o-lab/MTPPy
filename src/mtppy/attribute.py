class Attribute:
    def __init__(self, name, data_type, init_value, sub_cb=None):
        self.name = name
        self.type = data_type
        self.init_value = init_value
        self.value = init_value
        self.comm_obj = None
        self.sub_cb = sub_cb

    def set_value(self, value):
        if not self.validate_type(value):
            print('Cannot set value because of an incompatible type')
            return False

        self.value = self.convert_type(value)

        if self.sub_cb is not None:
            self.sub_cb(value)

        if self.comm_obj is not None:
            if self.comm_obj.write_value_callback is not None:
                self.comm_obj.write_value_callback(value)
        return True

    def validate_type(self, value):
        try:
            converted_value = self.type(value)
            return True
        except Exception:
            return False

    def convert_type(self, value):
        return self.type(value)

    def attach_communication_object(self, communication_object):
        self.comm_obj = communication_object
