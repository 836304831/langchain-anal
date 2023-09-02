# -*- encoding: utf-8 -*-
"""
@author: acedar  
@time: 2023/8/26 9:13
@file: unstructured_veirfy.py 
"""

import json
from unstructured.partition.auto import partition
elements = partition(filename="../datasets/unstructured_doc.md")


def print_ele(elements):
    for ele in elements:
        print("category:", f"{ele.category}")
        print("ele:", ele)
        # print("\n")


def convert2dict(elements):
    from unstructured.staging.base import convert_to_dict
    dict_data = convert_to_dict(elements)
    print("dict_data:\n", json.dumps(dict_data, ensure_ascii=False))


def convert2df(elements):
    from unstructured.staging.base import convert_to_dataframe

    df = convert_to_dataframe(elements)
    print("df.type:", type(df))
    print("cols:", list(df.columns))
    print(df.head())


# ************* 自动解析文档中的内容 ****************
# print_ele(elements)
# convert2dict(elements)
# convert2df(elements)


# ************* 自动解析文档中的内容 ****************

from unstructured.partition.csv import partition_csv
# 将csv文件的每行拼接在一起，作为一个doc返回
elements = partition_csv(filename="../datasets/检索数据demo.csv")
print("csv文件内容：")
print(elements[0].text[:200])

