import pymysql

from old_gtv.settings import *


class ReadCategories(object):
    def __init__(self):
        self.db = None
        self.cursor = None

        self.db = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PWD,
            database=MYSQL_DB,
            charset=MYSQL_CHAR
        )
        self.cursor = self.db.cursor()

    def _load_categories(self):
        _select = 'select * from `old_gtv`.`cates`'
        self.cursor.execute(_select)
        rows = self.cursor.fetchall()


if __name__ == "__main__":
    ReadCategories()
