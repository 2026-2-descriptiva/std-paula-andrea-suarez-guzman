import pandas as pd

def pregunta_08():
    tbl0 = pd.read_csv("data/tbl0.tsv", sep="\t")
    tbl0["suma"] = tbl0["c0"] + tbl0["c2"]
    return tbl0