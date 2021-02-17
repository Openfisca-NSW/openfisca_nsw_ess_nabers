# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class NABERS_BuildingType(Enum):
    apartment_building = 'Building is an apartment building.'
    data_centre = 'Building is a data centre.'
    hospital = 'Building is a hospital.'
    hotel = 'Building is a hotel.'
    office = 'Building is an office.'
    shopping_centre = 'Building is a shopping centre.'


class NABERS_building_type(Variable):
    value_type = Enum
    entity = Building
    possible_values = NABERS_BuildingType
    default_value = NABERS_BuildingType.office
    definition_period = ETERNITY
    label = 'What is the building type for the NABERS rated building?'


class postcode(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = "What is the postcode for the building you are calculating ESCs for?"
