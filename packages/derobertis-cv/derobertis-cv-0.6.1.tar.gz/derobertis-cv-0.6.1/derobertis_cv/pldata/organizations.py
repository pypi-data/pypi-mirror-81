from derobertis_cv.models.organization import Organization
from derobertis_cv.pldata.cover_letters.models import ApplicationTarget, HiringManager, Gender

SEC_DERA = Organization(
    'U.S. Securities and Exchange Commission',
    'Washington, DC',
    abbreviation='DERA',
    address_lines=[
        'Division of Economic and Risk Analysis',
        '100 F Street, NE',
        'Washington, DC 20549',
    ]
)

WYNETTA_JONES = HiringManager(
    'Jones',
    first_name='Wynetta',
    gender=Gender.FEMALE,
    title='Lead HR Specialist',
)

SEC_DERA_TARGET = ApplicationTarget(
    SEC_DERA,
    'Financial Economic Fellow',
    person=WYNETTA_JONES
)