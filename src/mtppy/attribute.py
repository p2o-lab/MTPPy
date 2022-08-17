import logging


class Attribute:
    def __init__(self, name: str, data_type, init_value, sub_cb=None):
        """
        Atttribute represents an elementary object (attribute or parameter) of a data assembly. Depending on whether
        subscription callback is defined or not, it might be an monitored object or a static OPC UA node.
        :param name: Attribute name.
        :param data_type: Attribute type.
        :param init_value: Initial value of the attribute.
        :param sub_cb: Subscription callback if applied.
        """
        self.name = name
        self.type = data_type
        corrected_value = self._correct_type(init_value)
        self.init_value = corrected_value
        self.value = corrected_value
        self.comm_obj = None
        self.sub_cb = sub_cb

    def set_value(self, value):
        """
        Set value of the attribute.
        :param value: Value.
        :return: Returns True if value was applied.
        """
        self.value = self._correct_type(value)

        if self.sub_cb is not None:
            self.sub_cb(self.value)

        if self.comm_obj is not None:
            if self.comm_obj.write_value_callback is not None:
                self.comm_obj.write_value_callback(self.value)

        logging.debug(f'New value for {self.name} is {self.value}')
        return True

    def _correct_type(self, value):
        """
        Converts a value to the attribute type.
        :param value: Value.
        :return: Converted value. If conversion is not possible, returns a default value of that type.
        """
        try:
            converted_value = self.type(value)
            return converted_value
        except Exception:
            return self.type()

    def attach_communication_object(self, communication_object):
        """
        Attach a communication object to the attribute, e.g. if an OPC UA node needs to be created for the attribute.
        :param communication_object: Communication object.
        :return:
        """
        self.comm_obj = communication_object
