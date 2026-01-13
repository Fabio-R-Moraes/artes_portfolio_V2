def is_a_positicve_number(value):
    try:
        number_string = float(value)
    except ValueError:
        return False
    
    return number_string > 0