# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

from pandas import pandas as pd
import numpy as np
float_formatter = "{:.9f}".format
np.set_printoptions(formatter={'float_kind':float_formatter})

# %% NAME OF ACTIVITY: Activity Definition B1 - Sell a High Efficiency Clothes Washing Machine


class is_clothes_washing_machine (Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'The End-User Equipment must be a clothes washing machine, as' \
            ' defined in AS/NZS 2040:2005 Performance of household' \
            ' electirical appliances - clothes washing machines.' # need to include conditions as defined in Standard.


class is_registered_for_energy_labelling (Variable):
        value_type = bool
        entity = Building
        definition_period = ETERNITY
        label = 'The Clothes Washing Machine must be registered for energy' \
                ' labelling.' # need to check if method guide defines what this means


class is_top_loader (Variable):
        value_type = bool
        entity = Building
        definition_period = ETERNITY
        label = 'Asks whether the relevant washing machine is a top loader' \
                ' washing machine.'


class is_front_loader (Variable):
        value_type = bool
        entity = Building
        definition_period = ETERNITY
        label = 'Asks whether the relevant washing machine is a front loader' \
                ' washing machine.'


class is_top_or_frontloader (Variable):
        value_type = bool
        entity = Building
        definition_period = ETERNITY
        label = 'The Clothes Washing Machine must be either a top loader or' \
                ' a front loader.'

    def formula(buildings, period, parameters):
        is_front_loader = buildings('is_front_loader', period)
        is_top_loader = buildings('is_top_loader', period)
        return is_front_loader + is_top_loader


class has_GEMS_recorded_load_in_KG (Variable):
        value_type = bool
        entity = Building
        definition_period = ETERNITY
        label = 'The Clothes Washing Machine must have a recorded load (in KG)' \
                ' in the GEMS Registry.'


class is_combination_washer_or_dryer (Variable):
        value_type = bool
        entity = Building
        definition_period = ETERNITY
        label = 'Asks whether the relevant washing machine is a combination' \
                ' washer or dryer.'
