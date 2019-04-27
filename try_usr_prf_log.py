import sqlite3
from usr_profile_lib.usr_profile_log import UserProfileLogger
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    profile_db = "usr_profile_db/user_profile.db"
    usr_email = "chlin3@kth.se"

    # ========================================================================
    conn = sqlite3.connect(profile_db)
    profile_logger = UserProfileLogger(usr_email, dbconn=conn)

    # log search
    profile_logger.log_search(
        query="zombie", query_type="intersection", ranking_type=None)
    profile_logger.log_search(
        query="zombie attack", query_type="phase", ranking_type=None)
    profile_logger.log_search(
        query="zombie attack", query_type="ranking", ranking_type="tf-idf")

    # log retrieved
    profile_logger.log_retrieved(
        selected_doc="Zombie_Walk.f"
    )

    # close db
    conn.close()