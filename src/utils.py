def calc_limite_peso(forca: int) -> int:
    base = 16

    if forca <= 0:
        return base - (forca * 2)
    elif forca >= 1:
        return base + (forca * 3)


def calc_hp(constituicao: int, classe: int, level: int) -> int:
    if classe == 0:
        base = 10
    elif classe == 1:
        base = 8
    elif classe == 2:
        base = 6
    return int(base + constituicao + ((level - 1) * (constituicao + base // 1.5)))
