import re
from typing import Any, List

import pandas as pd
from proture.utils import add_lists, explode
from proture.prepare.dataset.RefSeq import load_LRG_RefSeqGene

pd.set_option("display.max_columns", 100)


def parse_alternative_text(text: str):
    if pd.isna(text):
        return "default"
    else:
        pattern1 = r"Name=.*Displayed"
        search_result = re.search(pattern1, text)
        if search_result:
            iso_text = search_result.group()
            pattern2 = r"(?<=IsoId=).*(?=;)"
            search_result_2 = re.search(pattern2, iso_text)
            if search_result_2:
                return search_result_2.group()
            else:
                return "default"
        else:
            return "default"


def dict_RefSeq(x: str):
    if pd.isna(x):
        return {"default": []}
    else:
        re_sep = r"(?<=]);"
        is_isinstance_sep = re.search(r"(?<=]);", x)
        if is_isinstance_sep:
            isoform_RefSeq_mapping_dict = {}
            isoform_mapping: List[str] = re.split(r"(?<=]);", x)
            for isoform in isoform_mapping:
                if isoform != "":
                    split_isoform = isoform.split(" ")
                    if len(isoform.split(" ")) >= 2:
                        canonical, isoform_id = isoform.split(" ")
                    else:
                        canonical = isoform.strip(";")
                        isoform_id = "default"
                    isoform_id = isoform_id.strip("[").strip("]")
                    canonical = canonical.split(";")

                    if isoform_id not in isoform_RefSeq_mapping_dict.keys():
                        if isinstance(canonical, (list, tuple)):
                            isoform_RefSeq_mapping_dict[isoform_id] = canonical
                        else:
                            raise ValueError(
                                f"{canonical} is not list or tuple, please check"
                            )
                    else:
                        if isinstance(canonical, (list, tuple)):
                            isoform_RefSeq_mapping_dict[isoform_id] += canonical

            return isoform_RefSeq_mapping_dict

        else:
            return {
                "default": [i.strip("[").strip("]") for i in x.split(";") if i != ""]
            }


def UniProt2NP(
    homo_sapians_uniprot_df: pd.DataFrame, contain_all_uniprot_isoform: bool = False
):
    """UniProt Accession mapping to RefSeq Nucletide by LRG, see more at UniProt and LRG:https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/RefSeqGene/

    Args:
        homo_sapians_uniprot_df (pd.DataFrame): each row are UniProt Accession entry and must contain two fields of UniProt download result:1):RefSeq;2)Alternative products (isoforms)
        contain_all_uniprot_isoform (bool, optional): output result will contain all RefSeq associated with each UniProt Accession isoform or just the canonical isoform of this entry, if True, will contain RefSeq only if it really associated with canonical isoform of UniProt Accession entry. Defaults to False.

    Returns:
        _type_: _description_
    """
    # step1 parse the canonical isoforms of UniProt Accession and generate each isoform to RefSeq mapping
    homo_sapians_uniprot_df["canonical isoforms"] = homo_sapians_uniprot_df[
        "Alternative products (isoforms)"
    ].apply(lambda x: parse_alternative_text(x))
    homo_sapians_uniprot_df["canonical RefSeq"] = homo_sapians_uniprot_df[
        "RefSeq"
    ].apply(
        lambda x: dict_RefSeq(x)
    )  # type: ignore

    # step2 get canonical or all isoform of UniProt Accession to associated RefSeq
    def map2canonical(x):
        return pd.Series(
            {
                "canonical protein ID": x["canonical RefSeq"].get(
                    x["canonical isoforms"], None
                )
            }
        )

    if not contain_all_uniprot_isoform:
        homo_sapians_uniprot_df[
            "canonical RefSeq protein"
        ] = homo_sapians_uniprot_df.loc[
            :, ["canonical RefSeq", "canonical isoforms"]
        ].apply(
            lambda x: map2canonical(x), axis=1
        )
    else:
        homo_sapians_uniprot_df["canonical RefSeq protein"] = homo_sapians_uniprot_df[
            "canonical RefSeq"
        ].apply(
            lambda x: add_lists(list(x.values()))
        )  # type: ignore

    del homo_sapians_uniprot_df["canonical isoforms"]
    del homo_sapians_uniprot_df["canonical RefSeq"]
    # step3 explode multi-mapping relationship among canonical UniProt Accession and RefSeq to multi-row.
    homo_sapians_uniprot_df = homo_sapians_uniprot_df.explode(
        "canonical RefSeq protein"
    )

    # step 4 Convert NP to NM by LRG_RefSeqGene file
    LRG_RefSeqGene = load_LRG_RefSeqGene(
        local_dir="/p300s/wangmx_group/xutingfeng/statistic/proture/data/RefSeq/LRG_RefSeqGene"
    )
    NM2NP_mapping = (
        LRG_RefSeqGene.loc[:, ["RNA", "Protein"]].drop_duplicates().dropna(how="any")
    )

    hsapians_uniprot_NM = pd.merge(
        left=homo_sapians_uniprot_df.dropna(
            subset=["canonical RefSeq protein"], axis=0
        ),
        right=NM2NP_mapping,
        left_on="canonical RefSeq protein",
        right_on="Protein",
        how="inner",
    )

    print(
        f'now have gene:{len(explode(hsapians_uniprot_NM, column="Gene Names", sep =";")["Gene Names"].unique())} in the dataset'
    )
    return hsapians_uniprot_NM
