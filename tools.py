def toslugs(mass, u):
    """Convert lbm to slugs"""
    if u is 'lb':
        return mass * 0.031081
    elif u is 'kg':
        return mass * 0.06852177
    else:
        raise Exception("Unrecognized units")


def tofeet(x, u):
    """Convert inches to feet"""
    if u is 'cm':
        return x / 2.54
    elif u is 'in':
        return x / 12.0
    else:
        raise Exception("Unrecognized units")
