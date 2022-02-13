from mtppy.attribute import Attribute
from mtppy.suc_data_assembly import SUCIndicatorElement


class AnaView(SUCIndicatorElement):
    def __init__(self, tag_name, tag_description='', v_scl_min=0, v_scl_max=100, v_unit=0):
        super().__init__(tag_name, tag_description)

        self.v_scl_min = v_scl_min
        self.v_scl_max = v_scl_max
        self.v_unit = v_unit

        self._add_attribute(Attribute('V', float, init_value=0))
        self._add_attribute(Attribute('VUnit', int, init_value=self.v_unit))
        self._add_attribute(Attribute('VSclMin', float, init_value=self.v_scl_min))
        self._add_attribute(Attribute('VSclMax', float, init_value=self.v_scl_max))

    def set_v(self, value):
        self.attributes['V'].set_value(value)
        print('V set to %s' % value)


class BinView(SUCIndicatorElement):
    def __init__(self, tag_name, tag_description='', v_state_0='false', v_state_1='true'):
        super().__init__(tag_name, tag_description)

        self.v_state_0 = v_state_0
        self.v_state_1 = v_state_1

        self._add_attribute(Attribute('V', bool, init_value=False))
        self._add_attribute(Attribute('VState0', str, init_value=self.v_state_0))
        self._add_attribute(Attribute('VState1', str, init_value=self.v_state_1))

    def set_v(self, value):
        self.attributes['V'].set_value(value)
        print('V set to %s' % value)


class DIntView(SUCIndicatorElement):
    def __init__(self, tag_name, tag_description='', v_scl_min=0, v_scl_max=100, v_unit=0):
        super().__init__(tag_name, tag_description)

        self.v_scl_min = v_scl_min
        self.v_scl_max = v_scl_max
        self.v_unit = v_unit

        self._add_attribute(Attribute('V', int, init_value=0))
        self._add_attribute(Attribute('VUnit', int, init_value=self.v_unit))
        self._add_attribute(Attribute('VSclMin', int, init_value=self.v_scl_min))
        self._add_attribute(Attribute('VSclMax', int, init_value=self.v_scl_max))

    def set_v(self, value):
        self.attributes['V'].set_value(value)
        print('V set to %s' % value)


class StringView(SUCIndicatorElement):
    def __init__(self, tag_name, tag_description=''):
        super().__init__(tag_name, tag_description)

        self._add_attribute(Attribute('V', str, init_value=False))

    def set_v(self, value):
        self.attributes['V'].set_value(value)
        print('V set to %s' % value)
