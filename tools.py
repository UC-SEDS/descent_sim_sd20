def toslugs(x, u):
    """Convert to slugs"""
    cnst = {'lb': 0.031081,
            'kg': 0.06852177}
    try:
        return x*cnst[u]
    except KeyError:
        raise Exception("Unrecognized units (toslugs)")


def tofeet(x, u):
    """Convert to feet"""
    cnst = {'cm': 1.0 / 2.54,
            'in': 1.0 / 12.0}
    try:
        return x * cnst[u]
    except KeyError:
        raise Exception("Unrecognized units (tofeet)")

def tofps(x, u):
    cnst = {'mph': 1.4667}
    try:
        return x * cnst[u]
    except KeyError:
        raise Exception("Unrecognized units (tofps)")