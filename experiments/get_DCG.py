import pandas as pd
import numpy as np
import sys

if __name__ == '__main__':
    csv = sys.argv[1]
    df = pd.read_csv(csv, header=None, index_col=0)

    if len(df.columns) == 2:
        df.columns = ["name", "rel"]
    elif len(df.columns) == 3:
        df.columns = ["doc_id", "name", "rel"]
    else:
        raise ValueError("Wrong number of columns")
    df["idx"] = df.index + 1
    df["log2(i+1)"] = np.log2(df["idx"]+1)
    df["DCG"] = df["rel"] / df["log2(i+1)"]
    print("DCG@10 = ", np.sum(df["DCG"][:10]))
    print("DCG@20 = ", np.sum(df["DCG"][:20]))