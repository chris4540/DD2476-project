import sqlite3
from user_profile_lib.user_profile_logger import UserProfileLogger
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    conn = sqlite3.connect("user_profile_db/user_profile.db")
    profile_logger = UserProfileLogger('chlin3@kth.se', dbconn=conn)

    # log search
    profile_logger.log_search(
        query="zombie", query_type="intersection", ranking_type=None)
    profile_logger.log_search(
        query="zombie attack", query_type="phase", ranking_type=None)
    profile_logger.log_search(
        query="zombie attack", query_type="ranking", ranking_type="tf-idf")

    # close db
    conn.close()