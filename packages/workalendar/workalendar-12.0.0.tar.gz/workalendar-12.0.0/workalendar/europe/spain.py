from ..core import WesternCalendar
from ..registry_tools import iso_register


@iso_register('ES')
class Spain(WesternCalendar):
    'Spain'

    # Christian holidays
    include_epiphany = True
    include_immaculate_conception = True
    include_good_friday = True
    include_assumption = True
    include_all_saints = True

    # Civil holidays
    include_labour_day = True
    labour_day_label = "Día del trabajador"
    FIXED_HOLIDAYS = WesternCalendar.FIXED_HOLIDAYS + (
        (10, 12, "Fiesta nacional de España"),
        (12, 6, "Día de la Constitución Española")
    )


@iso_register('ES-CT')
class Catalonia(Spain):
    "Catalonia"

    include_easter_monday = True
    include_boxing_day = True
    boxing_day_label = "Sant Esteve"

    FIXED_HOLIDAYS = Spain.FIXED_HOLIDAYS + (
        (6, 24, "Sant Joan"),
        (9, 11, "Diada nacional de Catalunya"),
    )
