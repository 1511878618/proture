import re


def splitName2Attribution(x):
    """
    splitName2Attribution HGSV 命名法：https://varnomen.hgvs.org/recommendations/general/
    refSeq:https://en.wikipedia.org/wiki/RefSeq#:~:text=The%20Reference%20Sequence%20(RefSeq)%20database,was%20first%20introduced%20in%202000.

    Args:
        str类型: "NM_017547.4(FOXRED1):c.694C>T (p.Gln232Ter)"

    Returns:
        ["NM_017547.4", "Gln232Ter","694C>T"]
    """
    ref_pattern = r"[A-Za-z]+_[0-9]+[\.]*[0-9]*"
    AAS_pattern = r"(?<=(p.))[A-Za-z]{0,3}[^\s()]*"
    SNP_pattern = r"(?<=(c.))[\d]*[^\s()]*"
    ref = re.search(ref_pattern, x).group() if re.search(ref_pattern, x) else None
    AAS = re.search(AAS_pattern, x).group() if re.search(AAS_pattern, x) else None
    SNP = re.search(SNP_pattern, x).group() if re.search(SNP_pattern, x) else None
    return ref, AAS, SNP
