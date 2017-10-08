import traceback
from re import match

class FieldMixin():
    def type_validate(self, fields_type):
        result = {}
        if not fields_type:
            return
        for key, value in fields_type.items():
            if type(key) != value:
                result.update({key: False})
            else:
                result.update({key: True})
        return result

    def check_allowed_kwargs(self, allowed, **kwargs):
        kwargs = {key: value for key, value in kwargs.items() if key in allowed}
        return kwargs


class Field(FieldMixin):

    def __init__(self, name=None, primary_key=False, auto_increment=False, max_length=None,
                 unique=False, null=False, default=None):
        (filename,line_number,function_name,text)=traceback.extract_stack()[-3]
        self.name = name
        if not name:
            self.name = text[:text.find('=')].strip()[:]
        self.primary_key = primary_key
        self.max_length = max_length
        self.unique = unique
        self.null = null
        self.default = default
        self.auto_increment = auto_increment
        #if not (self.fields_type and self.required):
        self.fields_type, self.required = self._dynamic_vars()
        if not self._check_errors():
            raise KeyError('wrong field key or value: ' + str(self.required))

    def init_field(self, field_name):
        return field_name

    def _dynamic_vars(self):
        fields_type = {self.name: str}
        required = {'name': str}
        return fields_type, required

    def _check_errors(self, **kwargs):
        if not self.name:
            return
        if self.auto_increment and not self.primary_key:
            raise ValueError('AUTOINCREMENT works only with column PRIMARY KEY')
        validated_fields = self.type_validate(self.fields_type)
        for key, value in validated_fields.items():
            if value == False:
                raise TypeError('wrong argument value type: ' + str(key))

        if not match('^[a-zA-Z_][a-zA-Z0-9_]*$', self.name):
            raise ValueError(str(self.name) + ' table name is not allowed')
        return True

    def sql(self):
        name = '`'+self.name+'`'
        field = ' <field_type> '
        primary_key = ' PRIMARY KEY ' if self.primary_key else ''
        auto_increment = ' AUTOINCREMENT ' if self.auto_increment else ''
        null = 'NOT NULL' if not self.null else 'NULL'
        default = ' DEFAULT ' + str(self.default) + '' if self.default else ''
        res = name + field + primary_key + auto_increment + null + default
        return res


class CharField(Field):
    def __init__(self, *args, **kwargs):
        allowed = ('name', 'max_length', 'unique', 'null', 'default')
        kwargs = self.check_allowed_kwargs(allowed, **kwargs)
        super(CharField, self).__init__(*args, **kwargs)

    def _dynamic_vars(self):
        fields_type = {self.name: str, self.max_length: int}
        required = {'required':{'name': str, 'max_length': int},
                    'optional':{'default': str, 'null': bool, 'unique':bool}}
        return fields_type, required

    def _check_errors(self):
        if not self.max_length:
            return
        result = super(CharField, self)._check_errors()
        return False if not result else True

    @property
    def sql(self):
        sql_pattern = super(CharField, self).sql()
        sql_string = sql_pattern.replace('<field_type>', 'VARCHAR(' + str(self.max_length) + ')')
        return sql_string


class Integer(Field):
    def __init__(self, *args, **kwargs):
        allowed = ('name', 'primary_key', 'unique', 'null', 'default', 'auto_increment')
        kwargs = self.check_allowed_kwargs(allowed, **kwargs)
        super(Integer, self).__init__(*args, **kwargs)

    @property
    def sql(self):
        sql_pattern = super(Integer, self).sql()
        sql_string = sql_pattern.replace('<field_type>', 'INTEGER')
        return sql_string

class Text(Field):
    def __init__(self, *args, **kwargs):
        allowed = ('name','unique', 'null', 'default')
        kwargs = self.check_allowed_kwargs(allowed, **kwargs)
        super(Text, self).__init__(*args, **kwargs)

    @property
    def sql(self):
        sql_pattern = super(Text, self).sql()
        sql_string = sql_pattern.replace('<field_type>', 'TEXT')
        return sql_string

class Bool(Field):
    def __init__(self, *args, **kwargs):
        allowed = ('name', 'null', 'default')
        kwargs = self.check_allowed_kwargs(allowed, **kwargs)
        super(Bool, self).__init__(*args, **kwargs)

    def _dynamic_vars(self):
        fields_type = {self.name: str}
        required = {'required': {'name': str}, 'optional': {'default': bool}}
        return fields_type, required

    def _check_errors(self):
        if self.default not in [True, False]:
            return
        result = super(Bool, self)._check_errors()
        return False if not result else True

    @property
    def sql(self):
        self.default = 1 if self.default == True else 0
        sql_pattern = super(Bool, self).sql()
        sql_string = sql_pattern.replace('<field_type>', 'INTEGER')
        return sql_string