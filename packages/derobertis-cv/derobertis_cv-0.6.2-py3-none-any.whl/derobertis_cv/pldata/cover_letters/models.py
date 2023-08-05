from dataclasses import dataclass
from enum import Enum
from typing import Sequence, List, Optional

from pyexlatex.logic.format.and_join import join_with_commas_and_and
from pyexlatex.typing import PyexlatexItems, PyexlatexItem
import pyexlatex as pl

from derobertis_cv.models.organization import Organization
from derobertis_cv.plbuild.paths import DOCUMENTS_BUILD_PATH
from derobertis_cv.pldata.authors import Author, AUTHORS
from derobertis_cv.pldata.constants.authors import ANDY, NIMAL, BAOLIAN
from derobertis_cv.pldata.constants.contact import SITE_URL, EMAIL, PHONE, ADDRESS_LINES, NAME
from derobertis_cv.pldata.courses.fin_model import get_fin_model_course


class ApplicationComponents(str, Enum):
    CV = 'CV'
    JOB_MARKET_PAPER = 'Job market paper'
    OTHER_RESEARCH = 'Other research work'
    RESEARCH_STATEMENT = 'Research statement'
    TEACHING_STATEMENT = 'Teaching statement'
    COURSE_OUTLINES = 'Course outlines'
    TRANSCRIPTS = 'Graduate transcripts'
    EVALUATIONS = 'Teaching evaluations'


class ApplicationFocus(str, Enum):
    ACADEMIC = 'academic'
    GOVERNMENT = 'government'


class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'


@dataclass
class HiringManager:
    last_name: str
    first_name: Optional[str] = None
    gender: Optional[Gender] = None
    title: Optional[str] = None
    is_doctor: bool = False
    married: bool = False
    
    @property
    def prefix(self) -> str:
        if self.is_doctor:
            return 'Dr. '
        if self.gender == Gender.MALE:
            return f'Mr. '
        if self.gender == Gender.FEMALE:
            if self.married:
                return f'Mrs. '
            else:
                return f'Ms. '
        return ''

    @property
    def salutation_name(self) -> str:
        if not self.prefix:
            return self.full_name
        else:
            return f'{self.prefix}{self.last_name}'

    @property
    def full_name_with_prefix(self) -> str:
        return f'{self.prefix}{self.full_name}'

    @property
    def full_name_prefix_only_for_doctor(self) -> str:
        if self.is_doctor:
            return f'{self.prefix}{self.full_name}'
        return self.full_name
    
    @property
    def full_name(self) -> str:
        if self.first_name is None:
            return self.last_name
        else:
            return f'{self.first_name} {self.last_name}'


@dataclass
class ApplicationTarget:
    organization: Organization
    position_name: str
    person: HiringManager = HiringManager('Sir or Madam')


@dataclass
class CoverLetter:
    target: ApplicationTarget
    target_specific_content: PyexlatexItems
    included_components: Sequence[ApplicationComponents]
    focus: ApplicationFocus
    included_references: Sequence[Author] = (AUTHORS[ANDY], AUTHORS[NIMAL], AUTHORS[BAOLIAN])

    def to_pyexlatex(self, output: bool = True, out_folder: str = DOCUMENTS_BUILD_PATH) -> pl.LetterDocument:
        contents = [
            self.blue,
            self.intro_paragraph,
            *self.desire_content,
            self.app_package,
            self.action_paragraph,
        ]

        letter = pl.LetterDocument(
            contents,
            contact_info=[NAME, *ADDRESS_LINES],
            to_contact_info=self.to_contact_info,
            signer_name=NAME,
            salutation=f'Dear {self.target.person.salutation_name}:',
            packages=[
                pl.Package('geometry', modifier_str='margin=0.75in'),
                pl.Package('hyperref', modifier_str='hidelinks')
            ],
            font_size=11,
        )

        if output:
            letter.to_pdf(out_folder, outname=f'{self.target.organization.abbreviation} Cover Letter')

        return letter

    @property
    def to_contact_info(self) -> List[str]:
        contact_info = [
            self.target.person.full_name_prefix_only_for_doctor,
            self.target.organization.title,
        ]

        if self.target.organization.address_lines is not None:
            contact_info.extend(self.target.organization.address_lines)

        return contact_info

    @property
    def intro_paragraph(self) -> str:
        # TODO [#40]: a vs an for position
        return f"""
I am writing to express my interest and enthusiasm to be a {self.target.position_name} at 
{self.target.organization.abbreviation} and to submit my supporting application materials.
My name is {NAME} and I am a Ph.D. candidate in Finance at the University of Florida (expected summer 2021).
During the Ph.D., I produced four working papers, five works 
in progress, developed and taught two courses across six different semesters with 
up to 4.8/5 evaluations, and created 34 open
source software projects which improve the efficiency and reproducibility of empirical research.{self.site_footnote}
I have a unique set of skills that rarely overlap: a high competency in programming, econometrics, economic modeling, 
data science, and communication. {self.interest_sentence}
        """.strip()

    @property
    def interest_sentence(self) -> str:
        if self.focus == ApplicationFocus.ACADEMIC:
            return f"""
I want to bring my strong research and software pipeline, along with 
my high competency for teaching and fully developed Financial Modeling course{self.modeling_footnote} to 
{self.target.organization.abbreviation}.
            """.strip()
        elif self.focus == ApplicationFocus.GOVERNMENT:
            return ''
            return f"""
I want to bring all of these skills along with a strong work ethic to {self.target.organization.abbreviation}.
            """.strip()
        else:
            raise ValueError(f'no handling for focus {self.focus}')

    @property
    def desire_content(self) -> List[PyexlatexItem]:
        contents: List[PyexlatexItem] = []
        if self.focus == ApplicationFocus.ACADEMIC:
            contents.extend([self.research_overview, self.teaching_overview])
        elif self.focus == ApplicationFocus.GOVERNMENT:
            contents.append(self.government_overview)
        else:
            raise ValueError(f'no handling for focus {self.focus}')

        contents.append(self.target_specific_content)

        return contents

    @property
    def research_overview(self) -> str:
        return '[placeholder for research overview]'

    @property
    def teaching_overview(self) -> str:
        return '[placeholder for teaching overview]'

    @property
    def government_overview(self) -> str:
        return """
My research interests are broad but a central theme in nearly all of my projects is a 
focus on financial markets, whether it is analyzing 
the effects of government intervention, the role of both fundamental and 
behavioral information in price discovery, or the performance of assets. 
To support my research I have developed a technical skill set that allows me to 
uncover novel data sets through 
web-scraping and API access, work with large data sets, and build
machine learning models to make predictions and classifications. 
        """

    @property
    def app_package(self) -> PyexlatexItems:
        included_components_bullets = pl.MultiColumn(
            pl.UnorderedList([comp.value for comp in self.included_components]),
            3
        )

        return [
            "Within this application package, you will find the following components:",
            pl.VSpace(-0.2),
            included_components_bullets,
            pl.VSpace(-0.5),
        ]

    @property
    def action_paragraph(self) -> str:
        return f"""
In addition, as you will see in their supporting letters, submitted separately,
I come well-recommended from the esteemed professors on my dissertation committee, {self.recommenders_str}.
{self.application_action_sentence}
I would love to set up a call to discuss all the value I can add to {self.target.organization.abbreviation}. 
You can reach me at {EMAIL} any time or at {PHONE} during the hours of 7:00 AM - 7:00 PM, eastern. 
        """.strip()

    @property
    def application_action_sentence(self) -> str:
        sentence = 'Please take a look at my application materials as well as my '
        if self.focus == ApplicationFocus.ACADEMIC:
            sentence += 'personal and Financial Modeling websites.'
        elif self.focus == ApplicationFocus.GOVERNMENT:
            sentence += 'personal website.'
        else:
            raise ValueError(f'no handling for focus {self.focus}')
        return sentence

    @property
    def recommenders_str(self) -> str:
        return join_with_commas_and_and([author.name for author in self.included_references])

    @property
    def site_footnote(self) -> pl.Footnote:
        site_link = pl.Hyperlink(
            SITE_URL,
            pl.Bold(
                pl.TextColor(SITE_URL, color=self.blue)
            ),
        )
        site_footnote = pl.Footnote(['See more information on all of this at', site_link, 'or on my CV.'])
        return site_footnote

    @property
    def modeling_footnote(self) -> pl.Footnote:
        financial_modeling_url = get_fin_model_course().website_url
        modeling_link = pl.Hyperlink(
            financial_modeling_url,
            pl.Bold(
                pl.TextColor(financial_modeling_url, color=self.blue)
            ),
        )
        modeling_footnote = pl.Footnote(
            ['See the Financial Modeling course content at the course website: ', modeling_link])
        return modeling_footnote

    @property
    def blue(self) -> pl.RGB:
        return pl.RGB(50, 82, 209, color_name="darkblue")