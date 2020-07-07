

def update_query_object(query, data, exceptions=[]):
    """Iterates over given data object. Set attributes to SQLAlchemy query.

    Args:
        query (obj): SQLAlchemy query object
        data (obj): Given request's arguments from JSON
        exceptions (list): Keys for which iteration
                           should be skipped
    Returns:
        SQLAlchemy object:  Updated query object
    """
    for (k, v) in data.items():
        if k in exceptions:
            continue
        query.__setattr__(k, v)
    return query


def hasattr_or_fallback(obj, attribute, fallback):

    """Returns given object's attribute if it exists else
    returns given fallback

    Args:
        obj (obj): object on which we ask whether it has an attribute
        attribute (obj): attribute we ask if exists in object
        fallback (Any): value returned if object doesn't have asked attribute

    Returns:
        (Any): object's attrubte value
            or
        (Any): value set as fallback
    """

    if hasattr(obj, attribute):
        return obj[attribute]
    else:
        return fallback
