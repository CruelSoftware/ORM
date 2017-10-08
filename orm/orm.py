
def get_fields(model):
    fields = [f for f in model.__dict__ if not f.startswith('__')]
    return fields

def get_field(model, field):
    _field = getattr(model, field)
    return _field

def validate_fields(model):
    fields = get_fields(model)

def generate_sql(model):
    uniques = []
    table_name = (model.__name__).lower()
    sql = 'CREATE TABLE IF NOT EXISTS `' + table_name + '` ('
    fields = get_fields(model)
    for field in fields:
        _field = get_field(model, field)
        if _field.unique:
            uniques.append('CREATE UNIQUE INDEX IF NOT EXISTS '+table_name+'_'+_field.name+'_uindex ON '+ table_name +' ('+_field.name+');')
        sql += _field.sql + ', ' if fields[-1] != field else _field.sql
    sql += ');'

    for unique in uniques:
        sql+= unique

    return sql




