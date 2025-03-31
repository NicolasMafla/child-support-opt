def money_to_float(value: str|float) -> float:
    if isinstance(value, str):
        value = value.replace(",","")
    return float(value)