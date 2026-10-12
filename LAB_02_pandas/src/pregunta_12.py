import pandas as pd

def pregunta_12():
    tbl2 = pd.read_csv("data/tbl2.tsv", sep="\t")
    tbl2["c5"] = tbl2["c5a"] + ":" + tbl2["c5b"].astype(str)
    return (
        tbl2.groupby("c0")["c5"]
        .apply(lambda textos: ",".join(sorted(textos)))
        .reset_index()
    )