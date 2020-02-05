# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

# measured_electricity_consumption input at Step 1
# measured_gas_consumption input at Step 1
# onsite_unaccounted_electricity input at Step 1
# nabers_electricity input at Step 1
# hours_per_week_with_20_percent_occupancy input at Step 3
# net_lettable_area input at Step 3
# building_area_type input at Step 3

# coal_in_KG input in unit_conversions
# coal_KG_to_kWh input in unit_conversions
# diesel_in_L input in unit_conversions
# diesel_in_kWh KG input in unit_conversions
# gas_in_MJ input in unit_conversions
# gas_MJ_to_kWh input in unit_conversions

# add from filename import function to init.py

# note that this file is used to store variables which are IDENTICAL across NABERS office reverse calculators.


class f_tenancy(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "factor for tenancy NABERS calculation"

    def formula(buildings, period, parameters):
        adjusted_hours = buildings('maximum_nabers_adjusted_hours', period)
        return (1 / (0.38 + 0.0105 * adjusted_hours))

class test_coefficient_A(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "Rating equation coefficient_A used to calculate NABERS whole building ratings"

    def formula(buildings, period, parameters):
        state = buildings('building_state_location', period)
        rating_type = buildings('rating_type', period)
        return select(
            [state == "ACT" and rating_type == "whole_building"
            , state == "QLD" and rating_type == "whole_building"],
            [6.7605, 7.1]
            )
