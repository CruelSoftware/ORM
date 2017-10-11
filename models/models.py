from .fields import DataMixin
from connection import Connection
from sqlite3 import OperationalError



class Model(DataMixin):


    def __init__(self, db_instance: Connection = None, **kwargs):

        self.table_name = self.__class__.__name__.lower()
        self.state = 0
        if db_instance:
            self.db_instance = db_instance
        self.fields_list = [k for k in self.__class__.__dict__.keys() if not k.startswith('__')]
        self.check_allowed_kwargs(self.fields_list, **kwargs)
        fields_types = {k: v.type for k, v in self.__class__.__dict__.items() if not k.startswith('__') and k in kwargs}
        self.obj_fields = kwargs
        success = self.compare_validated(self.obj_fields, fields_types)
        if success:
            for key, value in self.obj_fields.items():
                field = value
                #field.value = value

    def __strict_check_fail(self, result):
        for item in result:
            query_res = item.split(':')[0]
            query = item.split(':')[1:]
            if query_res == 'FAIL':
                raise OperationalError('failed to execute: ' + str(query))

    def __smooth_check_fail(self, result):
        for item in result:
            query_res = item.split(':')[0]
            if query_res == 'FAIL':
                return
            else:
                return True

    def __find_primary_key_field(self):
        obj_field, pk_field = None, None
        for field in self.fields_list:
            f = getattr(self, field)
            if hasattr(f, 'primary_key') and f.primary_key == True:
                pk_field = field
        return pk_field

    @staticmethod
    def __set_value(f):
        if f.value == True:
            value = "1"
        elif f.value == False:
            value = "0"
        else:
            value = "{}{}{}".format('"', f.value, '"')
        return value

    def __get_fields_values(self, pk_field: str = None, all_fields: bool = False):
        fields, values = [], []
        for field in self.fields_list:
            if pk_field == field and not getattr(self, field).value:
                continue
            else:
                f = getattr(self, field)
                if f.value is not None and not all_fields:
                    fields.append(field)
                    values.append(self.__set_value(f))
                elif all_fields:
                    fields.append(field)
                    values.append(self.__set_value(f))
        fields = ', '.join(fields)
        values = ', '.join(values)

        return fields, values

    def __check_null(self, fields=None, pk_field=None):
        all_fields = list(self.fields_list)
        if pk_field:
            all_fields.remove(pk_field)
        fields_to_check = [field for field in all_fields if field not in fields]
        for field in fields_to_check:
            f = getattr(self, field)
            if not f.null:
                raise ValueError('field {} NULL is not allowed'.format(field))
        return None

    def __set_action(self):
        if self.state == 1:
            action = 'INSERT INTO'
        else:
            action = 'INSERT OR REPLACE INTO'
        return action

    def save(self):
        action = self.__set_action()
        pk_field = self.__find_primary_key_field()
        fields, values = self.__get_fields_values(pk_field)
        self.__check_null(fields.split(', '), pk_field)
        sql = '{} {} ({}) VALUES ({});'.format(action, self.table_name, fields, values)
        result, sql_res = self.db_instance.execute(sql)
        # TODO maybe do something with sql_res
        self.db_instance.commit()
        self.__strict_check_fail(result)

        return self

    @staticmethod
    def __dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    @staticmethod
    def __text_to_sql(text: str):
        sql = ''
        replace_dict = {'"True"': '1', '"False"': '0', 'True': '1', 'False': '0'}
        for key, value in replace_dict.items():
            sql = text.replace(key, value)
        return sql


    def select(self, fields_list: list = None, **kwargs):
        factory = self.__dict_factory
        self.check_allowed_kwargs(self.fields_list, **kwargs)
        fields, values = self.__get_fields_values(all_fields=True)
        if fields_list:
            dissalowed = [field for field in fields_list if field not in self.fields_list]
            if dissalowed:
                raise KeyError('not allowed fields in fields_list')
            else:
                fields = ', '.join(fields_list)

        sql_where = ''
        if kwargs:
            sql_str = 'and '.join(['{} = "{}"'.format(key, value) for (key, value) in kwargs.items()])
            sql_where = ' WHERE {}'.format(self.__text_to_sql(sql_str))
        sql = 'SELECT {} FROM {}{}'.format(fields, self.table_name, sql_where)
        cur = self.db_instance.conn_open()
        cur.row_factory = factory
        cur.execute(sql)
        object_list = list()
        objects = cur.fetchall()
        for object in objects:
            for key, value in object.items():
                setattr(self, key, value)
            setattr(self, 'state', 1)
            object_list.append(self)

        return objects if fields_list else object_list
