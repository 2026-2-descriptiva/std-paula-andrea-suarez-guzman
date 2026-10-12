from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import PercentFormatter


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """

    ventas = pd.read_csv("data/sales.csv.gz", parse_dates=["OrderDate"])
    ventas["order_month"] = ventas["OrderDate"].dt.to_period("M")

    # Cohorte: mes de la primera compra de cada cliente.
    ventas["cohort"] = ventas.groupby("CustomerID")["order_month"].transform("min")
    ventas["period_index"] = (
        (ventas["order_month"].dt.year - ventas["cohort"].dt.year) * 12
        + (ventas["order_month"].dt.month - ventas["cohort"].dt.month)
    )

    retencion = (
        ventas.groupby(["cohort", "period_index"])["CustomerID"]
        .nunique()
        .reset_index(name="active_customers")
    )
    tamanos = retencion.loc[
        retencion["period_index"] == 0, ["cohort", "active_customers"]
    ].rename(columns={"active_customers": "cohort_size"})
    retencion = retencion.merge(tamanos, on="cohort")
    retencion["retention_rate"] = (
        retencion["active_customers"] / retencion["cohort_size"]
    )
    retencion["cohort_month"] = retencion["cohort"].astype(str)
    retencion = retencion.sort_values(["cohort_month", "period_index"]).reset_index(
        drop=True
    )[
        [
            "cohort_month",
            "period_index",
            "active_customers",
            "cohort_size",
            "retention_rate",
        ]
    ]

    salida = Path("submission")
    salida.mkdir(parents=True, exist_ok=True)
    retencion.to_csv(salida / "cohort_retention.csv", index=False)

    # Mapa de calor: los periodos no observados quedan como NaN (celdas vacias).
    matriz = retencion.pivot(
        index="cohort_month", columns="period_index", values="retention_rate"
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    imagen = ax.imshow(
        np.ma.masked_invalid(matriz.to_numpy()), cmap="Blues", vmin=0, vmax=1
    )
    for fila in range(matriz.shape[0]):
        for columna in range(matriz.shape[1]):
            valor = matriz.iat[fila, columna]
            if pd.notna(valor):
                ax.text(
                    columna,
                    fila,
                    f"{valor:.0%}",
                    ha="center",
                    va="center",
                    color="white" if valor > 0.5 else "black",
                )
    ax.set_xticks(range(matriz.shape[1]), matriz.columns)
    ax.set_yticks(range(matriz.shape[0]), matriz.index)
    ax.set_xlabel("Meses desde la primera compra (period_index)")
    ax.set_ylabel("Cohorte (mes de la primera compra)")
    ax.set_title("Retención de clientes por cohorte")
    barra = fig.colorbar(imagen, ax=ax)
    barra.ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    fig.tight_layout()
    fig.savefig(salida / "cohort_retention_heatmap.png", dpi=150)
    plt.close(fig)

    return retencion
