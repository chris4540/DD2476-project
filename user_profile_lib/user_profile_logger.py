# import sqlite3
import logging
import time

logger = logging.getLogger('UserProfileLogger')

class UserProfileLogger:

    def __init__(self, user_email, dbconn=None):
        if dbconn is None:
            raise NotImplementedError("Not implemented to get connection from pool!")
        else:
            self.conn = dbconn

        self.user_id = self._get_user_id(user_email)
        logger.debug("Initialized UserProfileLogger: user_id = %d", self.user_id)

    def _get_user_id(self, user_email):
        sql = "SELECT id FROM users WHERE email='{}';".format(user_email)
        cur = self.conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()

        # parse user id
        ret = row[0]
        return ret

    def log_search(self, query, query_type, ranking_type=None):
        # build col_val dict
        col_val = {
            'userid': str(self.user_id),
            'posix_time': str(int(time.time())),
            'query': query,
            'query_type': query_type,
            'ranking_type': ranking_type
        }
        if ranking_type is None:
            col_val['ranking_type'] = "NULL"

        # create a sql with placeholder
        col = ','.join(col_val.keys())
        placeholders = ':'+', :'.join(col_val.keys())
        sql = "INSERT INTO user_search_log ({}) VALUES({});".format(col, placeholders)

        # execute the command
        cur = self.conn.cursor()
        cur.execute(sql, col_val)
        self.conn.commit()