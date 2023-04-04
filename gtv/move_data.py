import pymysql

from gtv.settings import *


class MoveData:
    def __init__(self):
        self.db = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PWD,
            database=MYSQL_DB,
            charset=MYSQL_CHAR
        )
        self.cursor = self.db.cursor()
        self._get_data_from_videos()

    def _get_data_from_videos(self):
        _page = 0
        _size = 1000
        _count = _size
        while _count >= _size:
            _sql = "select * from t_videos limit %d, %d" % (_page * _size, _size)
            try:
                self.cursor.execute(_sql)
                _rows = self.cursor.fetchall()
                for row in _rows:
                    _insert = "insert into t_videos_detail (`id`,`url`,`recommend`) values (%d, '%s', '%s')" % \
                              (row[0], row[1], row[10])
                    self.cursor.execute(_insert)
                self.db.commit()
                _page = _page + 1
                _count = len(_rows)
            except Exception as e:
                print(e)
            pass


if __name__ == "__main__":
    MoveData()
