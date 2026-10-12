import pandas as pd

def pregunta_06():
    tbl1 = pd.read_csv("data/tbl1.tsv", sep="\t")
    return sorted(tbl1["c4"].str.upper().unique().tolist())