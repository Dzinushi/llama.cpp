def str_to_bool(data):
    if isinstance(data, bool):
        return data
    elif isinstance(data, str):
        if data in ["true", "True", "Yes", "yes", "YES"]:
            return True
        if data in ["false", "False", "No", "no", "NO"]:
            return False
        else:
            raise ValueError(f"data value={data} don't recognized by str-2-bool converter")
    else:
        raise ValueError(f"data={data}, type={type(data)} must have type 'bool' or 'str'")
