import sqlite3
from user_profile_lib.user_profile_logger import UserProfileLogger
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    conn = sqlite3.connect("user_profile_db/user_profile.db")
    p = UserProfileLogger(conn, 'chlin3@kth.se')
    # c = conn.cursor()

    # c.execute("select id from users where email='chlin3@kth.se';")
    # row = c.fetchone()
    # print('2):', row)
    # conn.close()
