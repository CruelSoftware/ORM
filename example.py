import os

from models import Model, fields
from tables import create_table, drop_table
from connection import Connection

db_instance = Connection(os.path.join('.','db.sqlite3'))
Model.db_instance = db_instance


class User(Model):

    id = fields.Integer(primary_key=True, auto_increment=True)
    firstname = fields.CharField(max_length=30)
    lastname = fields.CharField(max_length=30, null=True)
    bio = fields.Text(null=True)
    years_old = fields.Integer(null=True)


class User1(Model):
    id = fields.Integer(primary_key=True, auto_increment=True)
    firstname = fields.CharField(max_length=30)
    lastname = fields.CharField(max_length=30, null=True)
    bio = fields.Text(null=True)
    years_old = fields.Integer(null=True)


db_instance.execute(create_table(User))
db_instance.execute(create_table(User1))
db_instance.execute(drop_table(User1))

user1 = User()
user1.firstname.value = 1
user1.lastname.value = 'Ivanov'
user1.save()

user2 = User(firstname='Sergei', lastname='Pavlov', bio='COOL GUY', years_old=22)
user2.save()

users = User().select()

users_filter = User().select(id=1, firstname='Ivan')
users_select_fields = User().select(fields_list=['id', 'firstname'])

