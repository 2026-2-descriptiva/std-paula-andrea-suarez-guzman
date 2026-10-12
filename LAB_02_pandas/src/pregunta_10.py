import pandas as pd

def pregunta_10():
    tbl0 = pd.read_csv("data/tbl0.tsv", sep="\t")
    return tbl0.groupby("c1")["c2"].apply(
        lambda valores: ":".join(str(valor) for valor in sorted(valores))
    ).to_frame()
