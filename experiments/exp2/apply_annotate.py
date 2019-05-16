import pandas as pd

if __name__ == "__main__":
    # apply for tempel
    annotate = pd.read_csv("tempel_rel.csv", header=None)
    annotate.columns = ["rel", "name"]
    annotate = annotate.set_index("name")
    rel_dict = annotate["rel"].to_dict()
    for i in range(1,5):
        f = "setting{}/tempel_query.csv".format(i)
        df = pd.read_csv(f, header=None, index_col=0)
        if len(df.columns) == 2:
            df.columns = ['doc_id', 'name']
        elif len(df.columns) == 3:
            df.columns = ['doc_id', 'name', 'rel']
        df['rel'] = df['name'].map(rel_dict, na_action='ignore')
        df.to_csv(f, header=False)

    # apply for the flygplats
    annotate = pd.read_csv("flygplats_rel.csv", header=None)
    annotate.columns = ["rel", "name"]
    annotate = annotate.set_index("name")
    rel_dict = annotate["rel"].to_dict()
    for i in range(1,5):
        f = "setting{}/flygplats_query.csv".format(i)
        df = pd.read_csv(f, header=None, index_col=0)
        if len(df.columns) == 2:
            df.columns = ['doc_id', 'name']
        elif len(df.columns) == 3:
            df.columns = ['doc_id', 'name', 'rel']
        df['rel'] = df['name'].map(rel_dict, na_action='ignore')
        df.to_csv(f, header=False)

    # apply for the slott
    annotate = pd.read_csv("slott_rel.csv", header=None)
    annotate.columns = ["rel", "name"]
    annotate = annotate.set_index("name")
    rel_dict = annotate["rel"].to_dict()
    for i in range(1,5):
        f = "setting{}/slott_query.csv".format(i)
        df = pd.read_csv(f, header=None, index_col=0)
        if len(df.columns) == 2:
            df.columns = ['doc_id', 'name']
        elif len(df.columns) == 3:
            df.columns = ['doc_id', 'name', 'rel']
        df['rel'] = df['name'].map(rel_dict, na_action='ignore')
        df.to_csv(f, header=False)