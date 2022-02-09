from src.attribute import Attribute
from src.suc_data_assembly import SUCIndicatorElement


class AnaView(SUCIndicatorElement):
    def __init__(self, tag_name, tag_description='', v_scl_min=0, v_scl_max=100, v_unit=0):
        super().__init__(tag_name, tag_description)

        self.control_elements = ControlElementsAnaView(v_scl_min=v_scl_min,
                                                       v_scl_max=v_scl_max,
                                                       v_unit=v_unit)


class ControlElementsAnaView:
    def __init__(self, v_scl_min, v_scl_max, v_unit):
        self.v_scl_min = v_scl_min
        self.v_scl_max = v_scl_max
        self.v_unit = v_unit

        self.attributes = {}
        self._init_attributes()

    def _init_attributes(self):
        self.attributes = {
            'V': Attribute('V', float, init_value=0),
            'VUnit': Attribute('VUnit', int, init_value=self.v_unit),
            'VSclMin': Attribute('VSclMin', float, init_value=self.v_scl_min),
            'VSclMax': Attribute('VSclMax', float, init_value=self.v_scl_max),
        }

    def set_v(self, value):
        self.attributes['V'].set_value(value)
        print('V set to %s' % value)
