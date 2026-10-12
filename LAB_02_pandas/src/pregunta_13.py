import pandas as pd

def pregunta_13():
    tbl0 = pd.read_csv("data/tbl0.tsv", sep="\t")
    tbl2 = pd.read_csv("data/tbl2.tsv", sep="\t")
    combinada = pd.merge(tbl0, tbl2, on="c0")
    return combinada.groupby("c1")["c5b"].sum()