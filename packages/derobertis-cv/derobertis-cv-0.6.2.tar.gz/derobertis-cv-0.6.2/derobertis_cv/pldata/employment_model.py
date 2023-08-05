import datetime
from dataclasses import dataclass
from typing import Any, Optional, Sequence

import pyexlatex.resume as lr
from pyexlatex.typing import PyexlatexItems

from derobertis_cv.models.course import CourseModel
from derobertis_cv.pldata.timelineable import Timelineable
from derobertis_cv.pltemplates.academic_employment import AcademicEmployment


@dataclass
class EmploymentModel(Timelineable):
    description: Sequence[str]
    company_name: str
    job_title: str
    location: str
    begin_date: datetime.date
    end_date: Optional[datetime.date] = None
    date_format: str = "%B %Y"
    latex_contents: Optional[PyexlatexItems] = None
    extra_contents: Optional[Any] = None
    company_short_name: Optional[str] = None
    short_job_title: Optional[str] = None

    def __post_init__(self):
        if self.latex_contents is None:
            self.latex_contents = [desc.replace('$', '\\$') for desc in self.description]

    @property
    def sort_key(self) -> datetime.date:
        if self.end_date is not None:
            return self.end_date
        return datetime.datetime.now()

    def to_pyexlatex_employment(self) -> lr.Employment:
        return lr.Employment(
            self.latex_contents,
            self.company_name,
            self.date_str,
            self.job_title,
            self.location,
        )


@dataclass
class AcademicEmploymentModel(EmploymentModel):
    courses_taught: Optional[Sequence[CourseModel]] = None

    def to_pyexlatex_employment(self) -> AcademicEmployment:
        return AcademicEmployment(
            self.latex_contents,
            self.company_name,
            self.date_str,
            self.job_title,
            self.location,
            self.courses_taught,
            self.extra_contents
        )