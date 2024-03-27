import config


def unit_converter(unit):
    match config.units:
        case "inches":
            return unit
        case 'cm':
            return unit / 2.54
        case 'mm':
            return unit / 25.4
        case 'feet':
            return unit * 12
        case 'meters':
            return unit * 39.37
