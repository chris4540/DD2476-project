class Config:
    index = "enwiki"
    # weightings / relative importance between term vector
    weights = {
        "title": 1.0,
        "category": 0.5,
        "text": 0.1,
    }
    # decaying factor / half life
    half_life = {
        "title": 12*3600,       # 12 hrs
        "category": 24*3600,    # 24 hrs
        "text": 3600            # 1 hr
    }

    elastic_host = "elastic.haochen.lu"
    # elastic_host = "localhost"

    doc_type = "page"  # TODO: add code comment for it

    if index == "enwiki":
        wiki_url_fmt = "http://en.wikipedia.org/wiki/{title}"
    elif index == "svwiki":
        wiki_url_fmt = "http://sv.wikipedia.org/wiki/{title}"

    doc_count = None     # place to store the doc count