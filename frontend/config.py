class Config:
    # index = "enwiki"
    index = "svwiki"
    # weightings / relative importance between term vector
    weights = {
        "title": 2.0,
        "category": 1.5,
        "text": 1.0,
        "query": 0.05,
    }
    # decaying factor / half life (in second)
    half_life = {
        "query": 7*3600,
        "title": 1*3600,
        "category": 2*3600,
        "text": 600,
    }

    elastic_host = "elastic.haochen.lu"
    elastic_port = "9200"
    timeout = 100
    # elastic_host = "localhost"

    doc_type = "page"  # TODO: add code comment for it

    if index == "enwiki":
        wiki_url_fmt = "http://en.wikipedia.org/wiki/{title}"
    elif index == "svwiki":
        wiki_url_fmt = "http://sv.wikipedia.org/wiki/{title}"

    expansion_size = 50
    feedback_weight = 1.0
    boost = {
        "title": 1.0,
        "text": 1.0
    }

    profile_weights = {
        "static": 0.3,
        "dynamic": 0.7,
    }

    static_info_to_profile = {
        "lang": 1.0,
        "city": 1.0,
        "country": 1.0,
    }

    weight_scheme = "tfidf"
    # the alpah value for re-ranking
    rerank_alpha = 0.7
    is_reorder_search_results = True  # reordering is a bit slow, option to turn it off