-- Build the user on the user table
INSERT INTO users(id, email, age, gender, lang, city, country)
VALUES (1, 'chlin3@kth.se', 26, 'M', 'Chinese', 'Hong Kong', 'China');
INSERT INTO users(id, email, age, gender, lang, city, country)
VALUES (2, 'testuser@kth.se', 22, 'M', 'Swedish', 'Stockholm', 'Sweden');
INSERT INTO users(id, email, age, gender, lang, city, country)
VALUES (3, 'dfsafd@kth.se', 22, 'M', 'Swedish', 'Stockholm', 'Sweden');
INSERT INTO users(id, email, age, gender, lang, city, country)
VALUES (4, 'antolu@kth.se', 22, 'M', 'Swedish', 'Stockholm', 'Sweden');
INSERT INTO users(id, email, age, gender, lang, city, country)
VALUES (5, 'liberman@kth.se', 22, 'M', 'Spanish', 'Stockholm', 'Sweden');

-- Add the basic information of the user interest as the static user profile
-- Start Chris Lin static profile
INSERT INTO user_profile_vector(userid, term, is_static, posix_time, score)
VALUES (1, "physics", 1, 0, 1.0);
INSERT INTO user_profile_vector(userid, term, is_static, posix_time, score)
VALUES (1, "mathematics", 1, 0, 1.0);
INSERT INTO user_profile_vector(userid, term, is_static, posix_time, score)
VALUES (1, "python", 1, 0, 1.0);
INSERT INTO user_profile_vector(userid, term, is_static, posix_time, score)
VALUES (1, "programming", 1, 0, 1.0);
-- End Chris Lin static profile

-- Start Test user profile
INSERT INTO user_profile_vector(userid, term, is_static, posix_time, score)
VALUES (2, "hitler", 1, 0, 10.0); -- 'hitler' : 10
INSERT INTO user_profile_vector(userid, term, is_static, posix_time, score)
VALUES (2, "albert", 1, 0, 5.0); -- 'albert' : 5,
INSERT INTO user_profile_vector(userid, term, is_static, posix_time, score)
VALUES (2, "speer", 1, 0, 3.0); -- 'speer' : 3,
INSERT INTO user_profile_vector(userid, term, is_static, posix_time, score)
VALUES (2, "java", 1, 0, 2.0); -- 'java' : 2,
INSERT INTO user_profile_vector(userid, term, is_static, posix_time, score)
VALUES (2, "programming", 1, 0, 2.0); -- 'programming' : 2
-- End Test user profile

-- dfsafd@kth.se static profile
INSERT INTO user_profile_vector(userid, term, is_static, posix_time, score)
VALUES (3, "programming", 1, 0, 1.0);

-- antolu@kth.se static profile
INSERT INTO user_profile_vector(userid, term, is_static, posix_time, score)
VALUES (4, "physics", 1, 0, 1.0);

-- liberman@kth.se static profile
INSERT INTO user_profile_vector(userid, term, is_static, posix_time, score)
VALUES (5, "travel", 1, 0, 1.0);
