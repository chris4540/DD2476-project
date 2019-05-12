class Config:
    index = "enwiki"
    # weightings / relative importance between term vector
    weights = {
        "query": 10.0,
        "title": 5.0,
        "category": 3,
        "text": 1.0,
    }
    # decaying factor / half life (in second)
    half_life = {
        "query": 5*3600,
        "title": 2*3600,
        "category": 3600,
        "text": 600,
    }

    elastic_host = "elastic.haochen.lu"
    # elastic_host = "localhost"

    doc_type = "page"  # TODO: add code comment for it

    if index == "enwiki":
        wiki_url_fmt = "http://en.wikipedia.org/wiki/{title}"
    elif index == "svwiki":
        wiki_url_fmt = "http://sv.wikipedia.org/wiki/{title}"

    expansion_size = 20
    feedback_weight = 1.0
    boost = {
        "title": 2.0,
        "text": 1.0
    }