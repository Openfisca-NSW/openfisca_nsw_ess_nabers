# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class has_valid_medicare_card(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "has a valid Medicare card"


class has_stayed_in_Out_Of_Care_Home(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "has been in Out of Home Care (OOHC)"


class currently_staying_in_Out_Of_Care_Home(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Is currently in Out of Home Care (OOHC)"
