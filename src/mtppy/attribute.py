class Attribute:
    def __init__(self, name: str, data_type, init_value, sub_cb=None):
        self.name = name
        self.type = data_type
        corrected_value = self.correct_type(init_value)
        self.init_value = corrected_value
        self.value = corrected_value
        self.comm_obj = None
        self.sub_cb = sub_cb

    def set_value(self, value):
        self.value = self.correct_type(value)

        if self.sub_cb is not None:
            self.sub_cb(self.value)

        if self.comm_obj is not None:
            if self.comm_obj.write_value_callback is not None:
                self.comm_obj.write_value_callback(self.value)

        print(f'New value for {self.name} is {self.value}')
        return True

    def correct_type(self, value):
        try:
            converted_value = self.type(value)
            return converted_value
        except Exception:
            return self.type()

    def attach_communication_object(self, communication_object):
        self.comm_obj = communication_object
