import polars as pl


def generate_summary_df_serial(dataframe):
    summary_results = []

    for col in dataframe.columns:
        col_series = dataframe[col]
        col_type = col_series.dtype

        # 初始化统计信息字典
        summary = {
            "Column": col,
            "Type": col_type,
            "Count": len(col_series),
            "Unique": len(col_series.unique()),
            "First": col_series[0],
            "Last": col_series[-1],
            "Nulls": col_series.null_count(),
        }

        # 处理数字列的统计信息
        if col_series.dtype.is_numeric():
            summary.update(
                {
                    "Max": col_series.max(),
                    "Min": col_series.min(),
                    "Mean": col_series.mean(),
                    "Std": col_series.std(),
                    "NaNs": col_series.is_nan().sum(),
                }
            )

        summary_results.append(summary)

    # Convert summary results to Polars DataFrame
    summary_df = pl.DataFrame(summary_results)
    return summary_df


# 将 summary_df 转换为 Markdown 表格
def to_markdown_table(df):
    markdown_table = "| " + " | ".join(df.columns) + " |\n"
    markdown_table += "| " + " | ".join(["---"] * len(df.columns)) + " |\n"

    for row in df.rows():
        markdown_table += "| " + " | ".join(map(str, row)) + " |\n"

    return markdown_table


if __name__ == "__main__":
    df = pl.read_csv("data\Aircraft1+MUOS_4_40887_UFO_4_23467.csv")

    summary_df = generate_summary_df_serial(df)
    markdown_table = to_markdown_table(summary_df)
    print(markdown_table)

    with pl.Config(tbl_rows=len(summary_df)):  # 显示全部的行
        print(summary_df)
