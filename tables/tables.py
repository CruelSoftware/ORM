def __get_fields(model):
    fields = [f for f in model.__dict__ if not f.startswith('__')]
    return fields

def __get_field(model, field):
    _field = getattr(model, field)
    return _field

def __validate_fields(model, fields):
    auto_increment_counter, primary_key_counter = 0, 0
    for field in fields:
        _field = __get_field(model, field)
        if getattr(_field, 'auto_increment', None):
            auto_increment_counter +=1
        if getattr(_field, 'primary_key', None):
            primary_key_counter +=1

    if auto_increment_counter > 1:
        raise KeyError('only 1 auto_increment field allowed')

    if primary_key_counter > 1:
        raise KeyError('only 1 primary_key field allowed')

    return True

def create_table(model):
    uniques = []
    table_name = (model.__name__).lower()
    sql = 'CREATE TABLE IF NOT EXISTS `' + table_name + '` ('
    fields = __get_fields(model)
    __validate_fields(model, fields)
    for field in fields:
        _field = __get_field(model, field)
        if _field.unique:
            uniques.append('CREATE UNIQUE INDEX IF NOT EXISTS {}_{}_uindex ON {} ({});'.format(table_name, str(field), table_name,str(field)))
        field_sql = _field.sql.replace('<placeholder>', str(field))
        sql += field_sql + ', ' if fields[-1] != field else field_sql
    sql += ');'

    for unique in uniques:
        sql+= unique
    message = 'table {} created'.format(table_name)
    return sql

def drop_table(model):
    table_name = model.__name__.lower()
    sql = 'DROP TABLE IF EXISTS '+ table_name
    message = 'table {} deleted'.format(table_name)
    return sql




