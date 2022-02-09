from src.attribute import Attribute
from src.suc_data_assembly import SUCIndicatorElement


class BinView(SUCIndicatorElement):
    def __init__(self, tag_name, tag_description='', v_state_0='false', v_state_1='true'):
        super().__init__(tag_name, tag_description)

        self.control_elements = ControlElementsBinView(v_state_0=v_state_0,
                                                       v_state_1=v_state_1)


class ControlElementsBinView:
    def __init__(self, v_state_0='false', v_state_1='true'):
        self.v_state_0 = v_state_0
        self.v_state_1 = v_state_1

        self.attributes = {}
        self._init_attributes()

    def _init_attributes(self):
        self.attributes = {
            'V': Attribute('VFbk', bool, init_value=False),
            'VState0': Attribute('VState0', str, init_value=self.v_state_0),
            'VState1': Attribute('VState1', str, init_value=self.v_state_1),
        }

    def set_v(self, value):
        self.attributes['V'].set_value(value)
        print('V set to %s' % value)
