-- Build the user on the user table
INSERT INTO users(id, email, age, gender, lang, city, country)
VALUES (1, 'chlin3@kth.se', 26, 'M', 'Chinese', 'Hong Kong', 'China');

-- Add the basic information of the user interest as the static user profile
INSERT INTO user_profile_vector_table(userid, keyword, is_static, posix_time, score)
VALUES (1, "physics", 1, 0, 1.0);
INSERT INTO user_profile_vector_table(userid, keyword, is_static, posix_time, score)
VALUES (1, "mathematics", 1, 0, 1.0);
INSERT INTO user_profile_vector_table(userid, keyword, is_static, posix_time, score)
VALUES (1, "python", 1, 0, 1.0);
INSERT INTO user_profile_vector_table(userid, keyword, is_static, posix_time, score)
VALUES (1, "functional programming", 1, 0, 1.0);