from derobertis_cv.models.university import UniversityModel
from derobertis_cv.pldata.constants.institutions import UF_NAME, VCU_NAME
from derobertis_cv.pltemplates.logo import image_base64

UF = UniversityModel(UF_NAME, 'Gainesville, FL', abbreviation='UF', logo_base64=image_base64('uf-logo.png'))
VCU = UniversityModel(VCU_NAME, 'Richmond, VA', abbreviation='VCU', logo_base64=image_base64('vcu-logo.png'))