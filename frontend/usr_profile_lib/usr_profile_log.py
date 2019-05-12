"""
Test this file in the folder of frontend
"""
import logging
import time
import sqlite3
from algorithm import aggregate_time_term_vecs
from config import Config

def row_factory(cursor, row):
    """
    """
    ret = {}
    for idx, col in enumerate(cursor.description):
        ret[col[0]] = row[idx]
    return ret

# FOR DEBUG USE
# logging.basicConfig(
#         filename='/var/log/usr_prof.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
#         level=logging.DEBUG)

logger = logging.getLogger('UserProfileLogger')
class UserProfileLogger:

    USER_PROFILE_DB = "../usr_profile_db/user_profile.db"

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        logger.debug("Closing the database connection")
        self.conn.close()

    def __init__(self, user_email):
        self.conn = sqlite3.connect(self.USER_PROFILE_DB)
        self.conn.row_factory = row_factory
        logger.debug("Using the profile database: %s", self.USER_PROFILE_DB)

        self.user_id = self._get_user_id(user_email)
        logger.debug("Initialized UserProfileLogger: user_id = %s", self.user_id)

    def _get_user_id(self, user_email):
        sql = "SELECT id FROM users WHERE email='{}';".format(user_email)
        cur = self.conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()

        if row is None:
            logger.debug(
                "User email %s not found in the database. No profiling for the user", user_email)
            ret = None
        else:
            # parse user id
            ret = row["id"]
        return ret

    @staticmethod
    def _insert_col_val_to_db_table(db_conn, table_name, col_val):

        # create a sql with placeholder
        col = ','.join(col_val.keys())
        placeholders = ':'+', :'.join(col_val.keys())
        sql = "INSERT INTO {} ({}) VALUES({});".format(table_name, col, placeholders)

        # execute the command
        cur = db_conn.cursor()
        cur.execute(sql, col_val)
        db_conn.commit()

    @staticmethod
    def _write_many_col_vals_to_db_table(db_conn, table_name, col_key, col_vals):
        """
        Args:
            col_key (list / tuple):
            col_vals (list of tuples):
        """
        col = ','.join(col_key)
        placeholders = ','.join(['?' for _ in col_key])
        sql = "INSERT OR REPLACE INTO {} ({}) VALUES({});".format(table_name, col, placeholders)

        cur = db_conn.cursor()
        cur.executemany(sql, col_vals)
        db_conn.commit()

    def log_search(self, query, query_type, ranking_type=None):
        if self.user_id is None:
            return

        # build col_val dict
        col_val = {
            'userid': str(self.user_id),
            'posix_time': str(int(time.time())),
            'query': query,
            'query_type': query_type,
            'ranking_type': ranking_type
        }
        # log the dictionary for debugging
        logger.debug('[user_search_log] profile: %s', col_val)
        self._insert_col_val_to_db_table(self.conn, "user_search_log", col_val)

    def log_retrieved(self, doc_id, index):
        if self.user_id is None:
            return
        col_val = {
            'userid': str(self.user_id),
            'posix_time': str(int(time.time())),
            'doc_id': doc_id,
            'index_': index
        }
        logger.debug('[user_retrieved_log] profile: %s', col_val)
        self._insert_col_val_to_db_table(self.conn, "user_retrieved_log", col_val)

    def _get_user_profile_rows(self, is_static=True, field=None):
        tbl = "user_profile_vector"
        cols = ','.join(['posix_time', 'term', 'score'])

        sql = ("SELECT {cols} FROM {tbl} WHERE userid=:uid "
               "AND is_static=:is_static".format(cols=cols, tbl=tbl))
        filter_val = {
            "uid": self.user_id,
            "is_static": is_static,
        }
        # ======================================================================
        if not is_static:
            sql += " AND field_=:field"
            filter_val['field'] = field

        cur = self.conn.cursor()
        cur.execute(sql, filter_val)
        rows = cur.fetchall()
        return rows

    def get_user_dynamic_profile_vec(self, field):
        """

        Return:
            return a term vector which is a function of time
            {
                "apple": {
                    "score": 10.0,
                    "posix_time": 1557608983
                },
                ...
            }
        """
        # Transform the rows to dict
        rows = self._get_user_profile_rows(is_static=False, field=field)
        ret = dict()
        for r in rows:
            row_dict = dict()
            for k in ['score', 'posix_time']:
                row_dict[k] = r[k]
            ret[r['term']] = row_dict
        return ret


    def log_term_vec_to_profile(self, term_vec, field):
        """
        log the term vector to a user profile as a dynamic part of the user profile
        Args:
            term_vec (dict): a term vector
                E.g.: {
                    'apple': 50.0,
                    'japan': 10.0,
                    ...
                }
            field (str): the field of the term vector.
                E.g. 'text', 'title', 'catagory'
        """
        col_key = ('userid', 'posix_time', 'is_static',
                   'field_', 'term', 'score',)
        # agg the dynamic profile to the term vec
        term_vec_t = self.get_user_dynamic_profile_vec(field)
        term_vec_now = aggregate_time_term_vecs(
            term_vec, term_vec_t, half_life=Config.half_life[field])

        # perpare some common values
        user_id = str(self.user_id)
        posix_time = str(int(time.time()))
        is_static = False

        # perpate column values
        col_vals = list()
        # only insert the updated components to reduce the cost of transcation
        for term in term_vec:
            score = term_vec_now[term]
            col_vals.append(
                (user_id, posix_time, is_static, field, term, score)
            )
        self._write_many_col_vals_to_db_table(
            self.conn, "user_profile_vector", col_key, col_vals)

if __name__ == "__main__":
    import sqlite3
    logging.basicConfig(level=logging.DEBUG)
    usr_email = "chlin3@kth.se"
    # Developers can alway change the profile db like this
    # UserProfileLogger.USER_PROFILE_DB = "myfoler/userprofile.db"
    # ========================================================================
    with UserProfileLogger(usr_email) as profile_logger:
        # # log search
        # profile_logger.log_search(
        #     query="zombie", query_type="intersection", ranking_type=None)
        # profile_logger.log_search(
        #     query="zombie attack", query_type="phase", ranking_type=None)
        # profile_logger.log_search(
        #     query="zombie attack", query_type="ranking", ranking_type="tf-idf")

        # # log retrieved
        # profile_logger.log_retrieved(doc_id="25609", index="enwiki")

        # log term vector
        profile_logger.log_term_vec_to_profile(
            {
                'computer': 10.0,
                'japan': 1.0
            }, field="title"
        )


        # fetch profile as term vector
        rows = profile_logger._get_user_profile_rows(is_static=True)
        rows = profile_logger.get_user_dynamic_profile_vec(field="title")
        # rows = profile_logger._get_user_profile_rows(is_static=False)
        # print(rows)

        vec = profile_logger.get_user_dynamic_profile_vec(field="title")
        # print(vec)
        # profile_logger.log_term_vec_to_profile(
        #     {'japan': 2.0}, field="title")
        vec = profile_logger.get_user_dynamic_profile_vec(field="title")
