import pandas as pd

def pregunta_01():
    tbl0 = pd.read_csv("data/tbl0.tsv", sep="\t")
    return len(tbl0)