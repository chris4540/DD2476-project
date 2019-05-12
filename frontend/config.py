class Config:
    index = "svwiki"
    # weightings / relative importance between term vector
    weights = {
        "title": 1.0,
        "category": 0.5,
        "text": 0.1,
    }
    # wiki_url_fmt = "http://en.wikipedia.org/wiki/{title}"
    wiki_url_fmt = "http://sv.wikipedia.org/wiki/{title}"
    elastic_host = "elastic.haochen.lu"
    # elastic_host = "localhost"