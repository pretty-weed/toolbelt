import scribus
from dandiscribe.enums import COLORS


COLOR_VALUES = {
    COLORS.LIGHT_BLUE: (64, 18, 0, 2),
    COLORS.PINK: (0, 31, 25, 4),
    COLORS.WHITE: (0, 0, 0, 0),
}
GREY_VAL = (
    sum(COLOR_VALUES[COLORS.LIGHT_BLUE]) // 4 + sum(COLOR_VALUES[COLORS.PINK])
) // 2
COLOR_VALUES[COLORS.GREY] = (GREY_VAL, GREY_VAL, GREY_VAL, GREY_VAL)

def register_colors():
    for color, values in COLOR_VALUES.items():
        if color in scribus.getColorNames():
            scribus.changeColorCMYK(color, *values)
        else:
            scribus.defineColorCMYK(color, *values)