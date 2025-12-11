#!/usr/bin/python3
# https://github.com/lukemorrill/tuxedo-backlight-control
# https://github.com/tuxedocomputers/tuxedo-keyboard

import os
import sys

from backlight_control import BacklightControl, backlight


def help():
    print("backlight <command> [<option>]")
    print("""
        Usage:
            -h, --help            Display this message

            off                   Turn off keyboard backlight

            <mode>                Set the keyboard backlight to <mode>, one of:
                                  breathe, cycle, dance, flash, random, tempo, wave

            color  <color>{1,4}   Set the keyboard backlight to a single color, one of:
                                  white, silver, gray, yellow, orange, red, maroon, crimson,
                                  fuchsia, purple, rose, cyan, turquoise, teal, blue, navy,
                                  olive, lime, green, OR any valid color_name=hex_value pairs
                                  defined in /etc/tuxedo-backlight-control/colors.conf

                                  Alternatively, set the keyboard to 4 distinct colors,
                                  in the order: left, center, right, extra. Only regions supported
                                  by your keyboard will have effect.

            brightness            Set keyboard backlight brightness from 0-255
    """)
    sys.exit()


if __name__ == "__main__":
    if len(sys.argv) == 1 or "--help" in sys.argv or "-h" in sys.argv:
        help()
    
    cmd = sys.argv[1]

    BacklightControl.validate_install()

    if cmd == "off":
        backlight.state = 0
        sys.exit()

    if len(sys.argv) == 2 and cmd in backlight.modes:
        backlight.state = 1
        backlight.mode = cmd

    if len(sys.argv) < 3:
        sys.exit(f"Error: No argument specified for '{cmd}'. Try 'backlight --help' to list available comamnds and valid arguments.")

    arg = sys.argv[2]
    if cmd == "brightness":
        backlight.state = 1
        try:
            arg = int(arg)

        except ValueError as error:
            sys.exit(f"Error: Invalid argument '{arg}' provided. Please provide a number from 0 - 255 to set brightness")

        if arg > 255 or arg < 0:
            sys.exit(f"Error: Invalid argument '{arg}' provided. Please provide a number from 0 - 255 to set brightness")

        backlight.brightness = str(arg)
    
    elif len(sys.argv) == 3 and cmd == "color" and arg in BacklightControl.colors.keys():
        backlight.state = 1
        backlight.set_single_color(arg)
    
    elif len(sys.argv) == 6:
        backlight.state = 1
        for index, region in enumerate(backlight.regions):
            setattr(backlight, "color_" + region, sys.argv[2 + index])
