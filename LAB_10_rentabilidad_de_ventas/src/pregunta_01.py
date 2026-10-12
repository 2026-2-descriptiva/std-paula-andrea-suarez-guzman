from pathlib import Path

import pandas as pd

def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """

    df = pd.read_csv(
        "data/superstore_orders.csv.gz",
        sep=";",
        decimal=",",
        encoding="utf-8-sig",
    )

    df["loss"] = df["Profit"] < 0
    df["lost_profit"] = -df["Profit"].where(df["loss"], 0)

    def resumir(grupo):
        return pd.Series(
            {
                "lines": len(grupo),
                "sales": grupo["Sales"].sum(),
                "profit": grupo["Profit"].sum(),
                "profit_margin": grupo["Profit"].sum() / grupo["Sales"].sum(),
                "loss_lines": grupo["loss"].sum(),
                "loss_line_rate": grupo["loss"].mean(),
                "lost_profit": grupo["lost_profit"].sum(),
            }
        )

    # 1. Resumen general.
    general = resumir(df)
    profitability_summary = pd.DataFrame(
        [
            {
                "lines": int(general["lines"]),
                "orders": df["Order ID"].nunique(),
                "sales": general["sales"],
                "profit": general["profit"],
                "profit_margin": general["profit_margin"],
                "loss_lines": int(general["loss_lines"]),
                "loss_line_rate": general["loss_line_rate"],
                "lost_profit": general["lost_profit"],
            }
        ]
    )

    # 2. Resumen por rango de descuento.
    rangos = ["0%", "1%-5%", "6%-10%", "más de 10%"]
    df["discount_band"] = pd.cut(
        df["Discount"],
        bins=[-float("inf"), 0, 0.05, 0.10, float("inf")],
        labels=rangos,
    )
    discount_summary = pd.DataFrame(
        [{"discount_band": rango, **resumir(df[df["discount_band"] == rango])} for rango in rangos]
    )
    discount_summary["lines"] = discount_summary["lines"].astype(int)
    discount_summary = discount_summary[
        [
            "discount_band",
            "lines",
            "sales",
            "profit",
            "profit_margin",
            "loss_line_rate",
            "lost_profit",
        ]
    ]

    # 3. Segmentos segmento-categoria que mas utilidad pierden.
    llaves = ["Customer Segment", "Product Category"]
    segmentos = pd.DataFrame(
        [
            {"Customer Segment": segmento, "Product Category": categoria, **resumir(grupo)}
            for (segmento, categoria), grupo in df.groupby(llaves)
        ]
    )
    segmentos["lines"] = segmentos["lines"].astype(int)
    priority_segments = (
        segmentos[segmentos["lines"] >= 100]
        .sort_values("lost_profit", ascending=False)
        .head(5)
        .reset_index(drop=True)[
            llaves + ["lines", "sales", "profit", "profit_margin", "lost_profit"]
        ]
    )

    salida = Path("submission")
    salida.mkdir(parents=True, exist_ok=True)
    profitability_summary.to_csv(salida / "profitability_summary.csv", index=False)
    discount_summary.to_csv(salida / "discount_summary.csv", index=False)
    priority_segments.to_csv(salida / "priority_segments.csv", index=False)

    return profitability_summary, discount_summary, priority_segments
