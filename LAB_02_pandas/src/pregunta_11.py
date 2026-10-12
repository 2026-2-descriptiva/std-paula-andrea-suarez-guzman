import pandas as pd

def pregunta_11():
    tbl1 = pd.read_csv("data/tbl1.tsv", sep="\t")
    return (
        tbl1.groupby("c0")["c4"]
        .apply(lambda letras: ",".join(sorted(letras)))
        .reset_index()
    )