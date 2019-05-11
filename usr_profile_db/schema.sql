DROP TABLE IF EXISTS user_profile_vector_table;
DROP TABLE IF EXISTS user_retrieved_log;
DROP TABLE IF EXISTS user_search_log;
DROP TABLE IF EXISTS users;
-- USER TABLE
CREATE TABLE users(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    email       TEXT                NOT NULL,
    age         INT                 NOT NULL,
    gender      CHAR(1)             NOT NULL,
    lang        TEXT                NOT NULL,
    city        TEXT                NOT NULL,
    country     TEXT                NOT NULL
);
-- USER search log table
CREATE TABLE user_search_log (
    id              INTEGER         PRIMARY KEY AUTOINCREMENT,
    userid          INTEGER         NOT NULL,
    posix_time      INTEGER         NOT NULL,
    query           TEXT            NOT NULL,
    query_type      CHAR(15)        NOT NULL,
    ranking_type    CHAR(10)        DEFAULT NULL,
    FOREIGN KEY(userid) REFERENCES users(id)
);
-- USER Retrieved page log table
CREATE TABLE user_retrieved_log (
    id              INTEGER         PRIMARY KEY AUTOINCREMENT,
    userid          INTEGER         NOT NULL,
    posix_time      INTEGER         NOT NULL,
    doc_id          TEXT            NOT NULL,
    index_          TEXT            NOT NULL,
    FOREIGN KEY(userid) REFERENCES users(id)
);
-- USER profile vector
-- TODO: improve the search by adding index when we know how the application
--       use the profile
CREATE TABLE user_profile_vector (
    userid          INTEGER         NOT NULL,
    posix_time      INTEGER         NOT NULL,
    is_static       BOOLEAN         NOT NULL,
    keyword         TEXT            NOT NULL,
    score           FLOAT           NOT NULL,
    PRIMARY KEY (userid, keyword, is_static),
    FOREIGN KEY(userid) REFERENCES users(id)
);