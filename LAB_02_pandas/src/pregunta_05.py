import pandas as pd

def pregunta_05():
    tbl0 = pd.read_csv("data/tbl0.tsv", sep="\t")
    return tbl0.groupby("c1")["c2"].max()
