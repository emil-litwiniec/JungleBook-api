

def update_query_object(query, data, exceptions):
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
