# class Model():
#     def __init__(self):
#         self.fields = {f for f in self.__dict__ if not f.startswith('__')}
#         for field in self.fields:
#             field.init_field(field.name)
#
#     def generate_sql(self):
#         sql_text = ''
#         for field in self.fields:
#             sql_text += field.sql
#         return sql_text
