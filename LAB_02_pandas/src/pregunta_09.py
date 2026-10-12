import pandas as pd

def pregunta_09():
    tbl0 = pd.read_csv("data/tbl0.tsv", sep="\t")
    tbl0["year"] = tbl0["c3"].str[:4]
    return tbl0