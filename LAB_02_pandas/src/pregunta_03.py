import pandas as pd

def pregunta_03():
    tbl0 = pd.read_csv("data/tbl0.tsv", sep="\t")
    return tbl0["c1"].value_counts().sort_index()