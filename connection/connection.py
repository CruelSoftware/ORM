import sqlite3


class Connection():

    def __init__(self, path):
        self.path = path
        self.connection = sqlite3.connect(self.path)

    def commit(self):
        return self.connection.commit()

    def conn_open(self):
        cursor = self.connection.cursor()
        self.description = cursor.description

        return cursor

    def conn_close(self):
        self.connection.close()
        return

    def execute(self, sql):
        results = []
        sql_res = None
        sql_list = sql.split(';')
        cursor = self.conn_open()
        for sql_item in sql_list:
            try:
                if sql_item != '':
                    sql_res = cursor.execute(sql_item + ';')
                    results.append('SUCCESS: {}...'.format(sql_item[:40]))
            except sqlite3.OperationalError as e:
                results.append('FAIL: {}...'.format(sql_item[:40]))
        return results, sql_res