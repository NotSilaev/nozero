def make_query_conditions(
    operator: str = "WHERE", 
    params_count: int = None, 
    null_columns: tuple = None,
    **kwargs
) -> tuple[str, tuple]:
    """
    Generates a string with sql query conditions and a tuple of parameters values.
    
    :param operator: `WHERE` is for standard conditions, `HAVING` is for aggregated conditions.
    :param **kwargs: column names and their values.
    """

    conditions_count = 0
    conditions = []
    params = []

    if null_columns:
        for column in null_columns:
            conditions.append(f"{column} IS NULL")

    for key, value in kwargs.items():
        if not value:
            continue
        conditions_count += 1
        conditions.append(f"{key} = ${conditions_count}")
        params.append(value)

    if conditions:
        if conditions_count > 1:
            where_string = " AND ".join(conditions)
        else:
            where_string: str = conditions[0]
        where_string = f"{operator.upper()} {where_string}"
    else:
        where_string = ""; params = tuple()

    conditions_data = (where_string, params)
    return conditions_data
