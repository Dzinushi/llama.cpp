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


def prompt_end_filter(output: str, filter_prompt_end: str = None):
    result = output
    if filter_prompt_end is not None:
        prompt_end_pos = output.find(filter_prompt_end)
        if prompt_end_pos != -1:
            result = output[:prompt_end_pos]
    return result
