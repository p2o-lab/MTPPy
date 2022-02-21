from src.mtppy.attribute import Attribute


def test_compatible_types():
    types = [int, float, str, bool]
    values = [-10, -5.6, 0, 1, 3.5, True, False]
    for data_type in types:
        for value in values:
            attr = Attribute(name='', data_type=data_type, init_value=value)
            assert (attr.value == data_type(value) or attr.value == data_type()) and isinstance(attr.value, data_type)

            attr.set_value(value)
            assert (attr.value == data_type(value) or attr.value == data_type()) and isinstance(attr.value, data_type)


def test_incompatible_types():
    types = [int, float]
    values = ['string']
    for data_type in types:
        for value in values:
            attr = Attribute(name='', data_type=data_type, init_value=value)
            assert (attr.value == data_type()) and isinstance(attr.value, data_type)

            attr.set_value(value)
            assert (attr.value == data_type()) and isinstance(attr.value, data_type)


class TestValue:
    def __init__(self):
        self.value = 0


def test_callback():
    test_value = TestValue()

    def callback_function(new_value):
        test_value.value = new_value

    attr = Attribute(name='', data_type=int, init_value=0, sub_cb=None)
    attr.set_value(10)
    assert test_value.value == 0

    attr = Attribute(name='', data_type=int, init_value=0, sub_cb=callback_function)
    attr.set_value(10)
    assert test_value.value == 10


class CommObj:
    def __init__(self):
        self.value = 0

    def write_value_callback(self, value):
        self.value = value


def test_communication_object_attachment():
    attr = Attribute(name='', data_type=int, init_value=10)
    comm_object = CommObj()
    attr.attach_communication_object(comm_object)
    assert attr.comm_obj == comm_object
    assert comm_object.value == 0
    attr.set_value(13)
    assert comm_object.value == 13
