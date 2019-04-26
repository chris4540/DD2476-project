DROP TABLE IF EXISTS user_search_log;
DROP TABLE IF EXISTS users;
-- USER TABLE
CREATE TABLE users(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    email       TEXT                NOT NULL,
    age         INT                 NOT NULL,
    gender      CHAR(1)             NOT NULL,
    lang        TEXT                NOT NULL
);
-- USER search log table
CREATE TABLE user_search_log(
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    userid          INTEGER,
    "posix_time"	INTEGER,
    action_         TEXT                NOT NULL,
    action_details  TEXT                NOT NULL, -- Changable
    FOREIGN KEY(userid) REFERENCES users(id)
)