def check_conditions(coord, conditions):
    """조건에 따라 좌표를 검사"""
    for condition in conditions:
        value = getattr(coord, condition.axis.lower())
        if not eval(f"{value} {condition.operator} {condition.value}"):
            return False
    return True
