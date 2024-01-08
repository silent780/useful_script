"""
@File    :   combine_pdf.py
@Time    :   2024/01/08 16:11:52
@Author  :   glx 
@Version :   1.0
@Contact :   18095542g@connect.polyu.hk
@Desc    :   use this script to combine sub-folder pdf files into one pdf file and name it as the sub-folder name
"""

# here put the import lib

# 导入 os 模块和 PyPDF2 模块
import os
from PyPDF2 import PdfMerger


# 定义一个函数，用于合并一个子文件夹中的所有 pdf 文件
def merge_pdf_in_folder(folder):
    # 创建一个 PdfFileMerger 对象
    merger = PdfMerger()
    # 获取子文件夹的名称，作为合并后的 pdf 文件的名称
    folder_name = os.path.basename(folder)
    # 遍历子文件夹中的所有文件
    for file in os.listdir(folder):
        # 如果文件是 pdf 格式，就将其添加到 merger 对象中
        if file.endswith(".pdf"):
            merger.append(os.path.join(folder, file))
    # 将 merger 对象中的所有 pdf 文件合并并保存到当前目录下，文件名为子文件夹的名称
    merger.write(folder_name + ".pdf")
    # 关闭 merger 对象
    merger.close()


# 定义一个函数，用于遍历一个文件夹中的所有子文件夹，并对每个子文件夹调用合并函数
def merge_pdf_in_subfolders(root):
    # 遍历根文件夹中的所有子文件夹
    for folder in os.listdir(root):
        # 如果是子文件夹，就调用合并函数
        if os.path.isdir(os.path.join(root, folder)):
            merge_pdf_in_folder(os.path.join(root, folder))


# 定义一个变量，表示要处理的文件夹的路径，您可以根据您的实际情况修改
root_folder = "."
# 调用遍历函数，对根文件夹中的所有子文件夹进行合并操作
merge_pdf_in_subfolders(root_folder)
