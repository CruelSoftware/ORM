import sqlite3

class Connection():

    def __init__(self, path):
        self.path = path
        self.connection = sqlite3.connect(self.path)

    def __conn_open(self):
        cursor = self.connection.cursor()
        return cursor

    def conn_close(self):
        self.connection.close()
        return

    def execute(self, sql):
        results = []
        sql_list = sql.split(';')
        cursor = self.__conn_open()
        for sql_item in sql_list:
            try:
                if sql_item != '':
                    cursor.execute(sql_item)
                    results.append('SUCCESS: ' + sql_item[:40]+ '...')
            except sqlite3.OperationalError as e:
                    results.append('FAIL: ' + sql_item[:40] + '...')
        return results

#sql = 'BEGIN TRANSACTION'
# sql = 'CREATE TABLE IF NOT EXISTS `user` (`id` INTEGER  PRIMARY KEY  AUTOINCREMENT NOT NULL, `bb` VARCHAR(20) NULL, `dd` INTEGER NOT NULL, `aa` VARCHAR(30) NOT NULL);CREATE UNIQUE INDEX IF NOT EXISTS user_bb_uindex ON user (bb);CREATE UNIQUE INDEX IF NOT EXISTS user_dd_uindex ON user (dd);'
# a = Connection('E:\codes\python\ORM\db.sqlite3')
# print(a.execute(sql))
# b = 3
