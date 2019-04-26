# import sqlite3
import logging

logger = logging.getLogger('UserProfileLogger')

class UserProfileLogger:

    def __init__(self, dbconn, user_email):
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