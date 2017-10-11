import os

from models import models, fields
from tables import create_table, drop_table
from connection import Connection

db_instance = Connection(os.path.join('.','db.sqlite3'))
models.Model.db_instance = db_instance


class User(models.Model):
    id = fields.Integer(primary_key=True, auto_increment=True)
    firstname = fields.CharField(max_length=30)
    lastname = fields.CharField(max_length=30, null=True)
    bio = fields.Text(null=True)
    years_old = fields.Integer(null=True)

    #def __init__(self):
    #    a = User.__dict__
    #    b = User.__class__
class User1(models.Model):
    id = fields.Integer(primary_key=True, auto_increment=True)
    firstname = fields.CharField(max_length=30)
    lastname = fields.CharField(max_length=30, null=True)
    bio = fields.Text(null=True)
    years_old = fields.Integer(null=True)


db_instance.execute(create_table(User))
db_instance.execute(create_table(User1))
db_instance.execute(drop_table(User1))

user1 = User()
user1.firstname = 1
user1.lastname = 'Ivanov'
user1.save()

user2 = User(firstname='Sergei', lastname='Pavlov', bio='COOL GUY', years_old=22)
user2.save()

users = User().select()

users_filter = User().select(id=1, firstname='Ivan')
users_select_fields = User().select(fields_list=['id', 'firstname'])

print('CHECK VARIABLES WITH DEBUGGER')
