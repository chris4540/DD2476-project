# import matplotlib.pyplot as plt
import pandas as pd


def plot_results(tsv):
    df = pd.read_csv(tsv, sep=",", index_col=0)
    df.index.name = "clicks"
    ax = df.plot(kind='line', style='x-')
    return ax
if __name__ == "__main__":


    # nDCG20
    ax = plot_results("nDCG20.csv")
    # relocate the lengend
    ax.legend(bbox_to_anchor=(1.1425, 1.03))
    ax.set_ylabel("nDCG score")
    # ax.set_title("Plot nDCG@20 against the number of clicks without query expansion")
    fig = ax.get_figure()
    fig.savefig("nDCG20_no_q_expand.png", bbox_inches='tight')
    fig.savefig("nDCG20_no_q_expand.eps", format="eps", bbox_inches='tight')
