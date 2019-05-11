-- Build the user on the user table
INSERT INTO users(id, email, age, gender, lang, city, country)
VALUES (1, 'chlin3@kth.se', 26, 'M', 'Chinese', 'Hong Kong', 'China');
INSERT INTO users(id, email, age, gender, lang, city, country)
VALUES (2, 'testuser@kth.se', 22, 'M', 'Swedish', 'Stockholm', 'Sweden');

-- Add the basic information of the user interest as the static user profile
-- Start Chris Lin static profile
INSERT INTO user_profile_vector(userid, keyword, is_static, posix_time, score)
VALUES (1, "physics", True, 0, 1.0);
INSERT INTO user_profile_vector(userid, keyword, is_static, posix_time, score)
VALUES (1, "mathematics", True, 0, 1.0);
INSERT INTO user_profile_vector(userid, keyword, is_static, posix_time, score)
VALUES (1, "python", True, 0, 1.0);
INSERT INTO user_profile_vector(userid, keyword, is_static, posix_time, score)
VALUES (1, "programming", True, 0, 1.0);
-- End Chris Lin static profile

-- Start Test user profile
INSERT INTO user_profile_vector(userid, keyword, is_static, posix_time, score)
VALUES (2, "hitler", True, 0, 10.0); -- 'hitler' : 10
INSERT INTO user_profile_vector(userid, keyword, is_static, posix_time, score)
VALUES (2, "albert", True, 0, 5.0); -- 'albert' : 5,
INSERT INTO user_profile_vector(userid, keyword, is_static, posix_time, score)
VALUES (2, "speer", True, 0, 3.0); -- 'speer' : 3,
INSERT INTO user_profile_vector(userid, keyword, is_static, posix_time, score)
VALUES (2, "java", True, 0, 2.0); -- 'java' : 2,
INSERT INTO user_profile_vector(userid, keyword, is_static, posix_time, score)
VALUES (2, "programming", True, 0, 2.0); -- 'programming' : 2
-- End Test user profile