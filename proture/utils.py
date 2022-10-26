import os
from copy import deepcopy
from functools import reduce
from typing import Any, List

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
