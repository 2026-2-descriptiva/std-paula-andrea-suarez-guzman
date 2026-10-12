import pandas as pd

def pregunta_02():
    tbl0 = pd.read_csv("data/tbl0.tsv", sep="\t")
    return tbl0.shape[1]
