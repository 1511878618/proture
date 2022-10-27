import os
from copy import deepcopy
from functools import reduce
from typing import Any, List
import re

import pandas as pd


def explode(df: pd.DataFrame, column: str, sep: str = ","):
    """explode the data~

    Args:
        df (pd.DataFrame): _description_
        column (str): _description_
        sep (str, optional): _description_. Defaults to ",".

    Returns:
        _type_: _description_
    """
    tmp = deepcopy(df)  # shallow copy

    tmp[column] = tmp[column].apply(lambda x: x.split(sep))
    return tmp.explode(column)


def add_lists(two_dimension_list: List[List[Any]]):
    """two_dimension_list should be two dimension like: [[1, 2], [3, 4]] and will return [1, 2, 3, 4]. this works like ``flatten(axis=0)``

    Args:
        two_dimension_list (List[List[Any]]): _description_

    Returns:
        _type_: _description_
    """
    return reduce(lambda x, y: x + y, two_dimension_list)


def mkdirs(path):
    try:
        os.makedirs(path)
    except:
        pass


def strip_comment_head(
    df: pd.DataFrame, comment: str = "#", inplace: bool = True
) -> pd.DataFrame:
    """去除header列可能存在的注释符号，如：#accession .... ，这里#可以是任意的comment符号

    Args:
        df (_type_): _description_
        comment (str, optional): _description_. Defaults to "#".
        inplace (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """
    if comment in df.columns[0]:  # type: ignore
        if inplace:
            df.rename(
                columns={
                    df.columns[0]: re.split(f"{comment}" + r"[\s]*", df.columns[0])[-1]  # type: ignore
                },
                inplace=True,
            )
        else:
            return df.rename(
                columns={
                    df.columns[0]: re.split(f"{comment}" + r"[\s]*", df.columns[0])[-1]  # type: ignore
                },
                inplace=False,
            )
    else:
        return df


def find_comment(file_path, header_comment_pattern="#"):
    """返回符合header_comment_pattern的最后一行的行号，从0开始。-1 表示没有找到匹配的注释行

    Args:
        file_path (_type_): _description_
        header_comment_pattern (str, optional): _description_. Defaults to "#".

    Returns:
        _type_: _description_
    """
    idx = 0
    for i in iter(open(file_path)):
        if not re.match(header_comment_pattern, i):
            return idx - 1
        else:
            idx += 1
