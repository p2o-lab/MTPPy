from src.attribute import Attribute
from src.suc_data_assembly import SUCIndicatorElement


class StringView(SUCIndicatorElement):
    def __init__(self, tag_name, tag_description=''):
        super().__init__(tag_name, tag_description)

        self.control_elements = ControlElementsStringView()


class ControlElementsStringView:

    def __init__(self):
        self.attributes = {}
        self._init_attributes()

    def _init_attributes(self):
        self.attributes = {
            'V': Attribute('VFbk', str, init_value=''),
        }

    def set_v(self, value):
        self.attributes['V'].set_value(value)
        print('V set to %s' % value)
