from algorithm import calcuate_term_vec_now
from algorithm import aggregate_term_vecs
from algorithm import filter_term_vec
from algorithm import get_sorted_term_vec
from algorithm import normalize_term_vec
from algorithm import weight_mean_term_vecs
from usr_profile_lib.usr_profile_log import UserProfileLogger
from config import Config
import matplotlib.pyplot as plt
from wordcloud import WordCloud
# https://github.com/googlefonts/noto-cjk/blob/master/NotoSansCJK-Regular.ttc
font = r'NotoSansCJK-Regular.ttc'  # need to download it


def plot_usr_word_cloud(email):
     # calculate the dynamic profile vector
    term_vecs_t = dict()
    with UserProfileLogger(email) as profile_logger:
        for f in Config.weights.keys():
            vec_t = profile_logger.get_user_dynamic_profile_vec(field=f)
            term_vecs_t[f] = vec_t

    # calculate term vector now
    term_vecs_now = dict()
    for f in term_vecs_t.keys():
        tvec_now = calcuate_term_vec_now(
            term_vecs_t[f], half_life=Config.half_life[f])
        term_vecs_now[f] = tvec_now
    term_vec = aggregate_term_vecs(term_vecs_now, Config.weights)
    term_vec = filter_term_vec(term_vec)
    dyn_profile_vec = get_sorted_term_vec(term_vec, limit=Config.expansion_size)
    dyn_profile_vec = normalize_term_vec(dyn_profile_vec)
    # End calculate the dynamic profiling

    # calculate the static profile
    with UserProfileLogger(email) as profile_logger:
        st_profile_vec = profile_logger.get_user_static_profile_vec()

    st_profile_vec = normalize_term_vec(st_profile_vec)
    expansion = weight_mean_term_vecs(
        st_profile_vec, dyn_profile_vec,
        Config.profile_weights["static"], Config.profile_weights["dynamic"])
    # normalize the expansion again
    expansion = normalize_term_vec(expansion)
    # ===========================================================================
    wcloud = WordCloud(font_path=font,
        background_color="white", width=1000, height=860, margin=2)
    wcloud.generate_from_frequencies(expansion)

    user_name = email.split("@")[0]
    wcloud.to_file('wcloud_{}.png'.format(user_name))

if __name__ == "__main__":
    emails = [
        # "chlin3@kth.se",
        # "dfsafd@kth.se",
        # "antolu@kth.se",
        # "liberman@kth.se",
        "testuser@kth.se"
    ]

    for email in emails:
        plot_usr_word_cloud(email)
