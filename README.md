# ORM
simple ORM to work with sqlite database (not for production usage for now)


Project contains 3 modules to work with, add to your project and
use like in example.py app, you will need sqlite database.

1. Module 'connection' contains Connection class

##### usage:
```
>> db_instance = Connection(path_to_database) # opens database instance
>> db_instance.execute(sql_query) # execute sql query
```
2. Module tables contains two functions:
##### create_table() - returns sql query which should create table on execute
##### drop_table() - returns sql query which should drop table on execute
3. Module models contains Model class and fields classes:

To add new model, create class inherited from Model as in example app.
Available fields for now: CharField, Integer, Text, Bool.
```
class User(Model):
    id = fields.Integer(primary_key=True, auto_increment=True)
    firstname = fields.CharField(max_length=30)
```
Execute query with create_table:
```
>> db_instance.execute(create_table(User))
```
To drop:
```
>> db_instance.execute(drop_table(User))
```

Also you may select and save data as in example app.

Fields are situated right in class, not in constructor, so this modules need rework before use in production,
something like model manager must be added, or maybe __getattr__ __setattr__ methods override (in this case all getters/setters in class
should be reworked to set attributes with __dict__ to avoid problems, values should be located in some kind of dictonary).