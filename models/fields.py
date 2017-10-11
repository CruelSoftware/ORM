import traceback
from re import match


class DataMixin():
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
        excluded = {key: value for key, value in kwargs.items() if key not in allowed}
        if excluded:
            raise KeyError('not allowed keyword argument(s) ' + str(excluded) + ' for ' + self.__class__.__name__)
        # kwargs = {key: value for key, value in kwargs.items() if key in allowed}
        return kwargs

    def check_validated(self, validated_fields):
        if validated_fields:
            for key, value in validated_fields.items():
                if value == False:
                    raise TypeError('wrong argument value type: ' + str(key) + ':' + str(type(key)))
        return True

    def compare_validated(self, obj_fields, fields_types):
        for key, value in obj_fields.items():
            if type(value) != fields_types[key]:
                raise TypeError(
                    'wrong field value type: ' + str(key) + ':' + str(fields_types[key]) + '=' + str(value) + ':' + str(
                        type(value)))
        return True


class Field(DataMixin):
    def __init__(self, primary_key: bool = False, auto_increment: bool = False, max_length: int = None,
                 unique: bool = False, null: bool = False, default=None):
        self.primary_key = primary_key
        self.max_length = max_length
        self.unique = unique
        self.null = null
        self.default = default
        self.auto_increment = auto_increment
        self.value = None
        # if not (self.fields_type and self.required):
        self.fields_type, self.required = self._dynamic_vars()
        if not self._check_errors():
            raise KeyError('wrong field key or value: ' + str(self.required))

    def _dynamic_vars(self):
        fields_type = {self.unique: bool, self.null: bool, self.auto_increment: bool, self.primary_key: bool}
        required = {'name': str}
        return fields_type, required

    def _check_errors(self, **kwargs):
        # if not self.name:
        #    return
        if self.auto_increment and not self.primary_key:
            raise ValueError('AUTOINCREMENT works only with column PRIMARY KEY')
        validated_fields = self.type_validate(self.fields_type)
        # if validated_fields:
        #     for key, value in validated_fields.items():
        #         if value == False:
        #             raise TypeError('wrong argument value type: ' + str(key))
        success = self.check_validated(validated_fields)

        # if not match('^[a-zA-Z_][a-zA-Z0-9_]*$', self.name):
        #    raise ValueError(str(self.name) + ' table name is not allowed')
        return success

    def sql(self):
        name = '`<placeholder>`'
        field = ' <field_type> '
        primary_key = ' PRIMARY KEY ' if self.primary_key else ''
        auto_increment = ' AUTOINCREMENT ' if self.auto_increment else ''
        null = 'NOT NULL' if not self.null else 'NULL'
        default = ' DEFAULT ' + str(self.default) + '' if self.default else ''
        res = "{}{}{}{}{}{}".format(name, field, primary_key, auto_increment, null, default)
        return res


class CharField(Field):
    def __init__(self, *args, **kwargs):
        allowed = ('name', 'max_length', 'unique', 'null', 'default', 'primary_key')
        kwargs = self.check_allowed_kwargs(allowed, **kwargs)
        super(CharField, self).__init__(*args, **kwargs)

    def _dynamic_vars(self):
        fields_type = {self.max_length: int, self.unique: bool, self.null: bool, self.auto_increment: bool,
                       self.primary_key: bool}
        required = {'required': {'name': str, 'max_length': int},
                    'optional': {'default': str, 'null': bool, 'unique': bool}}
        return fields_type, required

    def _check_errors(self):
        if not self.max_length:
            return
        result = super(CharField, self)._check_errors()
        return False if not result else True

    @property
    def type(self):
        return str

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
    def type(self):
        return int

    @property
    def sql(self):
        sql_pattern = super(Integer, self).sql()
        sql_string = sql_pattern.replace('<field_type>', 'INTEGER')
        return sql_string


class Text(Field):
    def __init__(self, *args, **kwargs):
        allowed = ('name', 'unique', 'null', 'default')
        kwargs = self.check_allowed_kwargs(allowed, **kwargs)
        super(Text, self).__init__(*args, **kwargs)

    @property
    def type(self):
        return str

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
        fields_type = {self.default: bool, self.unique: bool, self.null: bool, self.auto_increment: bool,
                       self.primary_key: bool}
        required = {'required': {'name': str}, 'optional': {'default': bool}}
        return fields_type, required

    def _check_errors(self):
        if self.default not in [True, False]:
            return
        result = super(Bool, self)._check_errors()
        return False if not result else True

    @property
    def type(self):
        return bool

    @property
    def sql(self):
        self.default = 1 if self.default == True else 0
        sql_pattern = super(Bool, self).sql()
        sql_string = sql_pattern.replace('<field_type>', 'INTEGER')
        return sql_string
