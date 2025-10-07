def filter_dict_keys(data: dict, allowed_keys: set) -> dict:
    return {k: v for k, v in data.items() if k in allowed_keys}
