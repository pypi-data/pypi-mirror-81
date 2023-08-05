from typing import List

from derobertis_cv.pldata.authors import AUTHORS
from derobertis_cv.pldata.constants.authors import NIMAL, ANDY
from derobertis_cv.pldata.cover_letters.models import CoverLetter, ApplicationComponents, ApplicationFocus
from derobertis_cv.pldata.organizations import SEC_DERA_TARGET


def get_cover_letters() -> List[CoverLetter]:
    return [
        CoverLetter(
            SEC_DERA_TARGET,
            [
"""
I believe I have an ideal fit with being a Financial Economic Fellow at DERA because 
I have research related to valuation, corporate finance, and economic policy, and technical 
skills related to developing economic models and 
extracting then communicating insights from large quantities of data.
I have a strong interest in the regulation of financial markets and would enjoy doing
my part towards determining the appropriate policies and their enforcement. Further, 
I have a locational preference towards Washington, DC as my family lives in Northern Virginia,
though I would not rule out any of the other locations. 
""",
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.TRANSCRIPTS,
                ApplicationComponents.JOB_MARKET_PAPER
            ],
            focus=ApplicationFocus.GOVERNMENT,
            included_references=(AUTHORS[ANDY], AUTHORS[NIMAL])
        ),
    ]