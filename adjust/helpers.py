def tokenize_query(query):
    query_params = {}
    try:
        for q in query.split(';'):
            key, values = q.split(':', 1)
            if not key.startswith('date'):
                values = values.split(',')
            query_params[key] = values
        return query_params, None
    except (ValueError, AttributeError):
        return None, True
