import pdfplumber
import pandas as pd


def extract_table_data(page):
    table_data = []

    # 提取表格数据
    for table in page.extract_tables():
        for row in table:
            table_data.append(row)

    return table_data


def pdf_to_excel(input_pdf, output_excel):
    # 打开PDF文件
    with pdfplumber.open(input_pdf) as pdf:
        all_table_data = []

        # 提取每个页面的表格数据
        for page in pdf.pages:
            table_data = extract_table_data(page)
            all_table_data.extend(table_data)

    # 创建DataFrame
    df = pd.DataFrame(all_table_data)

    # 保存为Excel文件
    df.to_excel(output_excel, index=False)


# 指定输入PDF文件路径和输出Excel文件路径
input_pdf = "your_pdf_file.pdf"
output_excel = "output_excel_file.xlsx"

# 调用函数进行转换
pdf_to_excel(input_pdf, output_excel)
