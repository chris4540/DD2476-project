import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv("nDCG10.csv", index_col=0)
    df.index.name = "Dynamic profile ratio (β)"
    ax = df.plot(kind='bar', rot=0)
    ax.set_ylabel("nDCG score")
    ax.set_ylim([0, 1])
    fig = ax.get_figure()
    fig.savefig("nDCG10_exp3.png", bbox_inches='tight')
    fig.savefig("nDCG10_exp3.svg", format="svg", bbox_inches='tight')

    df = pd.read_csv("nDCG20.csv", index_col=0)
    df.index.name = "Dynamic profile ratio (β)"
    ax = df.plot(kind='bar', rot=0)
    ax.set_ylabel("nDCG score")
    ax.set_ylim([0, 1])
    fig = ax.get_figure()
    fig.savefig("nDCG20_exp3.png", bbox_inches='tight')
    fig.savefig("nDCG20_exp3.svg", format="svg", bbox_inches='tight')
