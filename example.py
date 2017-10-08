from models import models, fields
from orm import generate_sql
from connection import Connection

class User():
    #def __init__(self):
    #    super(User).__init__()

    id = fields.Integer(primary_key=True, auto_increment=True)
    field1 = fields.CharField(max_length=30)
    field2 = fields.CharField(max_length=20, null=True, unique=True)
    field3 = fields.Integer(unique=True)
    field4 = fields.Text(unique=True, default='asdasd')
    field5 = fields.Bool(unique=True, default=True)

# class User1(models.Model):
#     id1 = fields.Integer(primary_key=True, auto_increment=True)
#     field1 = fields.CharField(max_length=30)
#     field2 = fields.CharField(max_length=20, null=True, unique=True)
#     field3 = fields.Integer(unique=True)
#     field4 = fields.Text(unique=True, default='asdasd')
#     field5 = fields.Bool(unique=True, default=True)

#print(generate_sql(User))
db_instance = Connection('E:\codes\python\ORM\db.sqlite3')
db_instance.execute(generate_sql(User))
#db_instance.execute(generate_sql(User1))
