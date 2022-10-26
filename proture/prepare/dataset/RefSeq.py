from typing import List, Literal, Union
import pandas as pd
from proture.download.utils import download_url
from proture import DEFAULT_DOWNLOAD_PATH
import os.path as osp


def load_LRG_RefSeqGene(
    local_dir: Union[str, None] = None,
    save_dir: str = osp.join(DEFAULT_DOWNLOAD_PATH, "LRG_RefSeqGene"),
):
    if local_dir is None:
        # see https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/RefSeqGene/
        url = "https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/RefSeqGene/LRG_RefSeqGene"
        download_url(url=url, output_file=save_dir)
        local_dir = save_dir

    return pd.read_csv(local_dir, index_col=False, sep="\t")
