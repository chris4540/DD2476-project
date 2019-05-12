class Config:
    index = "enwiki"
    # weightings / relative importance between term vector
    weights = {
        "title": 3.0,
        "category": 2,
        "text": 0.5,
        "query": 10,
    }
    # decaying factor / half life (in second)
    half_life = {
        "title": 2*3600,
        "category": 3600,
        "text": 600,
        "query": 12*3600
    }

    elastic_host = "elastic.haochen.lu"
    # elastic_host = "localhost"

    doc_type = "page"  # TODO: add code comment for it

    if index == "enwiki":
        wiki_url_fmt = "http://en.wikipedia.org/wiki/{title}"
    elif index == "svwiki":
        wiki_url_fmt = "http://sv.wikipedia.org/wiki/{title}"

