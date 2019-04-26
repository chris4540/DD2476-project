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
CREATE TABLE IF NOT EXISTS user_search_log (
	id	            INTEGER         PRIMARY KEY AUTOINCREMENT,
	userid	        INTEGER         NOT NULL,
	posix_time	    INTEGER         NOT NULL,
	query	        TEXT            NOT NULL,
	query_type	    CHAR(15)        NOT NULL,
	ranking_type	CHAR(10)		DEFAULT NULL,
	FOREIGN KEY(userid) REFERENCES users(id)
);
-- CREATE TABLE IF NOT EXISTS "user_retrival_log" (
-- 	"id"	INTEGER,
-- 	"userid"	INTEGER
-- );