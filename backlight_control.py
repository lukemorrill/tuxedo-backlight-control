import sys
import re
from pathlib import Path


class BacklightControl():
    """
    Abstraction on top of tuxedo_keyboard C driver interface for keyboard backlight
    """

    DEVICE_PATH = Path('/sys/devices/platform/tuxedo_keyboard/')
    MODULE_PATH = Path('/sys/module/tuxedo_keyboard')
    VERSION = '0.8.0'

    modes = (
        'color',
        'breathe',
        'cycle',
        'dance',
        'flash',
        'random',
        'tempo',
        'wave'
    )

    colors = {
        'aqua': '00FFFF',
        'blue': '0000FF',
        'crimson': 'DC143C',
        'fuchsia': 'FF00FF',
        'gray': '808080',
        'green': '008000',
        'lime': '00FF00',
        'maroon': '800000',
        'navy': '000080',
        'olive': '808000',
        'orange': 'FFA500',
        'pink': 'FFC0CB',
        'purple': '800080',
        'red': 'FF0000',
        'silver': 'C0C0C0',
        'teal': '008080',
        'turquoise': '40E0D0',
        'white': 'FFFFFF',
        'yellow': 'FFFF00'
    }

    regions = ('left', 'center', 'right', 'extra')
    
    params = (
        'state',
        'mode',
        'color_left',
        'color_center',
        'color_right',
        'color_extra',
        'brightness'
    )

    @staticmethod
    def validate_install():
        """
        Ensure the Tuxedo keyboard module is installed.
        """
        if not BacklightControl.DEVICE_PATH.exists():
            print(f"Error: The tuxedo_keyboard module is not installed at {BacklightControl.DEVICE_PATH}")
            sys.exit(1)

    @staticmethod
    def get_device_param(prop: str) -> str | None:
        """ read driver param value directly from '/sys/devices/platform/tuxedo_keyboard/' """
        prop_file = BacklightControl.DEVICE_PATH / prop
        return prop_file.readtext() if prop_file.exists() else None

    @staticmethod
    def get_device_color(region: str):
        """ read driver color value directly from '/sys/devices/platform/tuxedo_keyboard/' """

        color = BacklightControl.get_device_param('color_' + region)
        if color:
            try:
                index = list(BacklightControl.colors.values()).index(color.strip().upper())
                return list(BacklightControl.colors.keys())[index]
            except Exception:
                return 'Select...'
        return None

    @staticmethod
    def set_device_param(prop: str, value: str):
        (BacklightControl.DEVICE_PATH / prop).write_text(value)

    @staticmethod
    def set_device_color(region: str, color: str):
        if color in BacklightControl.colors.keys():
            index = list(BacklightControl.colors.values()).index(color.strip().upper())
            values = list(BacklightControl.colors.keys())
            BacklightControl.set_device_param('color_' + region, values[index])

    @staticmethod
    def find_color_by_key(color: str):
        index = list(BacklightControl.colors.keys()).index(color)
        return '0x' + list(BacklightControl.colors.values())[index]

    @staticmethod
    def is_single_color():
        """ checks whether all keyboard regions have the same color assigned to them """
        is_single = True
        last_color = None

        for region in BacklightControl.regions:
            color = BacklightControl.get_device_color(region)
            if last_color not in (None, color):
                is_single = False
                break
            last_color = color

        return is_single

    @staticmethod
    def set_single_color(color:str):
        """ assigns a single color by name to all keyboard regions """
        for region in BacklightControl.regions:
            mapped_color = BacklightControl.find_color_by_key(color)
            BacklightControl.set_device_param('color_' + region, mapped_color)

    @staticmethod
    def capitalize(label: str):
        """ capitalizes a string """
        return label.capitalize()

    @property
    def state(self):
        param = self.get_device_param('state')
        if param:
            return int(param)
        return 1

    @state.setter
    def state(self, value: int):
        self.set_device_param('state', str(value))

    @property
    def mode(self):
        param = self.get_device_param('mode')
        if param and len(self.modes) > int(param):
            return self.modes[int(param)]
        return None

    @mode.setter
    def mode(self, value: str):
        index = self.modes.index(value)
        self.set_device_param('mode', str(index))

    @property
    def color_left(self):
        """ get hex code for color_left """
        return self.get_device_color('left')

    @color_left.setter
    def color_left(self, value: str):
        """ set hex code for color_left, with color name present in colors dict """
        self.set_device_param('color_left', self.find_color_by_key(value))

    @property
    def color_center(self):
        """ get hex code for color_center """
        return self.get_device_color('center')

    @color_center.setter
    def color_center(self, value: str):
        """ set hex code for color_center, with color name present in colors dict """
        self.set_device_param('color_center', self.find_color_by_key(value))

    @property
    def color_right(self):
        """ get hex code for color_right """
        return self.get_device_color('right')

    @color_right.setter
    def color_right(self, value: str):
        """ set hex code for color_right, with color name present in colors dict """
        self.set_device_param('color_right', self.find_color_by_key(value))

    @property
    def color_extra(self):
        """ get hex code for color_extra """
        return self.get_device_color('extra')

    @color_extra.setter
    def color_extra(self, value: str):
        """ set hex code for color_extra, with color name present in colors dict """
        self.set_device_param('color_extra', self.find_color_by_key(value))

    @property
    def brightness(self):
        """ get brightness value """
        return self.get_device_param('brightness')

    @brightness.setter
    def brightness(self, value: int):
        """ set brightness value """
        self.set_device_param('brightness', value)

    @staticmethod
    def display_modes():
        """ return a capitalized item-list of all backlight modes """
        return map(BacklightControl.capitalize, BacklightControl.modes)

    @staticmethod
    def display_colors():
        """ return a capitalized item-list of all backlight colors """
        return map(BacklightControl.capitalize, BacklightControl.colors.keys())

backlight = BacklightControl()
