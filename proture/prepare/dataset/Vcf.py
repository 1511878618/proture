import pandas as pd
from proture.utils import find_comment, strip_comment_head
from proture.prepare.mutation.utils import is_missense_mutant_at_HGVSp

import re
import vcfpy


class VEP_PARSER:
    def __init__(self, vep_info_header: vcfpy.header.InfoHeaderLine) -> None:
        self.vep_col = self.parse_vep_header_parse(vep_info_header)

    @staticmethod
    def parse_vep_header_parse(vep_info_header):
        if match := re.search(r"(?<=Format:).*", vep_info_header.description):
            vep_col = match.group().split("|")
            return vep_col

        else:
            raise ValueError(f"can't find any col of vep at {vep_info_header}")

    def apply(self, vep_line_str: str):
        vep_line_list = vep_line_str.split("|")
        if len(vep_line_list) != len(self.vep_col):
            # raise ValueError(f"{vep_line_str} is not match with {self.vep_col}")
            return {}
        else:
            return dict(zip(self.vep_col, vep_line_list))

    def filter(self, func, vep_info: list, how: str = "all"):
        """
        apply vep_info will be a dict with vep_col in the vep_parser. the func accept input is a dict, which key are vep_col and values are vep_info, and output True of False, which decide this indices of vep_info drop or keep.

        Args:
            func (_type_): _description_
            vep_info (list): _description_
        Example:
            import vcfpy

            reader = vcfpy.Reader.from_path(gnomAD_path)
            vep_parser = VEP_PARSER(reader.header.get_info_field_info("vep"))

            vep_parser.filter(lambda x: print(x) if x["CANONICAL"] != "" else None, a.INFO["vep"])
        Returns:
            List:

        """
        out = []
        for vep_line in vep_info:
            vep_parse_result = self.apply(vep_line)
            if not vep_parse_result:
                raise ValueError(f"{vep_line} is not match with {self.vep_col}")

            if func(vep_parse_result):
                out.append(vep_line)

                if how == "any":
                    break
                elif how == "all":
                    continue
                else:
                    raise ValueError(f"{how} is not any or all")

        return out
        # func

    def __repr__(self) -> str:
        return "\t".join(self.vep_col)
