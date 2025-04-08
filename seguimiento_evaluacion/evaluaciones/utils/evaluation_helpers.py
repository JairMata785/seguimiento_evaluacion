def get_qualitative_rating(score):
    if score >= 4.5:
        return "EXCELENTE"
    elif score >= 4.0:
        return "NOTABLE"
    elif score >= 3.5:
        return "BUENO"
    elif score >= 3.0:
        return "REGULAR"
    elif score >= 2.0:
        return "SUFICIENTE"
    else:
        return "NO SUFICIENTE"