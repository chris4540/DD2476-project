# import matplotlib.pyplot as plt
import pandas as pd


def plot_results(tsv):
    df = pd.read_csv(tsv, sep="\t", index_col=0)
    df.index.name = "clicks"
    ax = df.plot(kind='line', style='x-')
    return ax
if __name__ == "__main__":

    # # nDCG10
    # ax = plot_results("nDCG10.tsv")
    # ax.set_ylabel("nDCG score")
    # # ax.set_title("Plot nDCG@10 against the number of clicks")
    # fig = ax.get_figure()
    # fig.savefig("nDCG10.png", bbox_inches='tight')
    # fig.savefig("nDCG10.eps", format="eps", bbox_inches='tight')
    # # plt.cla()
    # nDCG20
    ax = plot_results("nDCG20.tsv")
    ax.set_ylabel("nDCG score")
    ax.set_ylim([0, 1])
    # ax.set_title("Plot nDCG@20 against the number of clicks")
    fig = ax.get_figure()
    fig.savefig("nDCG20.png", bbox_inches='tight')
    fig.savefig("nDCG20.eps", format="eps", bbox_inches='tight')

    # Prec10
    # ax = plot_results("Prec10.tsv")
    # ax.set_ylabel("Precision")
    # # ax.set_title("Plot Precision at 10 against the number of clicks")
    # fig = ax.get_figure()
    # fig.savefig("Prec10.png", bbox_inches='tight')
    # fig.savefig("Prec10.eps", format="eps", bbox_inches='tight')

    # Prec20
    ax = plot_results("Prec20.tsv")
    ax.set_ylabel("Precision")
    ax.set_ylim([0, 1])
    # ax.set_title("Plot Precision at 20 against the number of clicks")
    ax.legend(bbox_to_anchor=(1, .93))
    fig = ax.get_figure()
    fig.savefig("Prec20.png", bbox_inches='tight')
    fig.savefig("Prec20.eps", format="eps", bbox_inches='tight')
