import os

def get_env_variable(name_variable, default_variable = ''):
    return os.environ.get(name_variable, default_variable)

def parse_comma_str_to_list(comma_str):
    if not comma_str or not isinstance(comma_str, str):
        return []
    
    return[string.strip() for string in comma_str.split(',') if string]