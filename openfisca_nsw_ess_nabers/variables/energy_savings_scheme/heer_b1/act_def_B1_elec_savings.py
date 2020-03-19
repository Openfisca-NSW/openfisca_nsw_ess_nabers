# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

from pandas import pandas as pd
import numpy as np
float_formatter = "{:.9f}".format
np.set_printoptions(formatter={'float_kind':float_formatter})

# %% NAME OF ACTIVITY: Activity Definition B1 - Sell a High Efficiency Clothes Washing Machine


class WashingMachineStarRating(Enum):
    '0.5 star' = u"Washing machine has a 0.5 star energy star rating"
    '1 star' = u"Washing machine has a 1 star energy star rating"
    1.5 = u"Washing machine has a 1.5 star energy star rating"
    2 = u"Washing machine has a 2 star energy star rating"
    2.5 = u"Washing machine has a 2.5 star energy star rating"
    3 = u"Washing machine has a 3 star energy star rating"
    3.5 = u"Washing machine has a 3.5 star energy star rating"
    4 = u"Washing machine has a 4 star energy star rating"
    4.5 = u"Washing machine has a 4.5 star energy star rating"
    5 = u"Washing machine has a 5 star energy star rating"
    5.5 = u"Washing machine has a 5.5 star energy star rating"
    6 = u"Washing machine has a 6 star energy star rating"
    6.5 = u"Washing machine has a 6.5 star energy star rating"
    7 = u"Washing machine has a 7 star energy star rating"
    7.5 = u"Washing machine has a 7.5 star energy star rating"
    8 = u"Washing machine has a 8 star energy star rating"
    8.5 = u"Washing machine has a 8.5 star energy star rating"
    9 = u"Washing machine has a 9 star energy star rating"
    9.5 = u"Washing machine has a 9.5 star energy star rating"
    10 = u"Washing machine has a 10 star energy star rating"


class machine_star_rating(Variable):
    value_type = Enum
    possible_values = WashingMachineStarRating
    default_value = WashingMachineStarRating
    entity = Building
    definition_period = ETERNITY
    label = u'The building type of the NABERS rating building, as entered by' \
            ' the user.'


class load_weight_kg(Variable):
        value_type = float
        entity = Building
        definition_period = ETERNITY
        label = 'The weight of the load for the relevant washing machine, in' \
                ' KG.'


class b1_deemed_equip_elec_savings(Variable):
        value_type = float
        entity = Building
        definition_period = ETERNITY
        label = 'The Deemed Equipment Electricity Savings for the activity,' \
                ' in MWh per washing machine sold.'

    def formula(buildings, period, parameters) # need to convert this to dictionary
        star_rating = buildings('machine_star_rating', period)
        load_weight = buildings('load_weight_kg', period)
