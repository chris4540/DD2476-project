from algorithm import calcuate_term_vec_now
from algorithm import aggregate_term_vecs
from usr_profile_lib.usr_profile_log import UserProfileLogger
from config import Config
import matplotlib.pyplot as plt
from wordcloud import WordCloud

if __name__ == "__main__":
    usr_email = "chlin3@kth.se"
    term_vecs_t = dict()
    with UserProfileLogger(usr_email) as profile_logger:
        for f in ['text', 'title', 'category']:
            vec_t = profile_logger.get_user_dynamic_profile_vec(field=f)
            term_vecs_t[f] = vec_t

    # calculate term vector now
    term_vecs_now = dict()
    for f in term_vecs_t.keys():
        tvec_now = calcuate_term_vec_now(
            term_vecs_t[f], half_life=Config.half_life[f])
        term_vecs_now[f] = tvec_now

    # agg differnet kind of term vector into one
    term_vec = aggregate_term_vecs(term_vecs_now, Config.weights)
    # ===========================================================================
    wcloud = WordCloud(background_color="white",width=1000, height=860, margin=2)
    wcloud.generate_from_frequencies(term_vec)
    plt.imshow(wcloud)
    plt.axis("off")
    plt.show()
    wcloud.to_file('test.png')

