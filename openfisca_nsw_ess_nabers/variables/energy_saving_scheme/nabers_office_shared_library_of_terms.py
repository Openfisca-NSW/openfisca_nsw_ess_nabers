# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *
import numpy as np
float_formatter = "{:.9f}".format
np.set_printoptions(formatter={'float_kind':float_formatter})

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

# note that this file is used to store variables which are IDENTICAL across
# NABERS office reverse calculators. This file is to be made PRIVATE.


class nabers_adjusted_hours(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "NABERS adjusted hours of building operations"

    def formula(buildings, period, parameters):
        input_hours = buildings('hours_per_week_with_20_percent_occupancy', period)
        return (input_hours + 10)


class maximum_nabers_adjusted_hours(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Maximum allowable NABERS adjusted hours of building operations - maximum number of hours in week is 168"

    def formula(buildings, period, parameters):
        condition_maximum_hours = buildings('nabers_adjusted_hours', period) >= 168
        return where(condition_maximum_hours, 168, buildings('nabers_adjusted_hours', period))


class climate_zone(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Climate zone value for the relevant climate zone, determined by the' \
            ' the relevant postcode.'

    def formula(buildings, period, parameters):
        postcode = buildings('postcode', period)
        return parameters(period).energy_saving_scheme.test_output_climate_zones[postcode]  # This is a built in OpenFisca function that is used to calculate a single value for regional network factor based on a zipcode provided


class HDD_18(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'HDD value for the relevant climate zone, determined by the' \
            ' the relevant postcode.'

    def formula(buildings, period, parameters):
        postcode = buildings('postcode', period)
        return parameters(period).energy_saving_scheme.test_output_hdd[postcode]  # This is a built in OpenFisca function that is used to calculate a single value for regional network factor based on a zipcode provided


class CDD_15(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "The relevant cooling days for this building, based on postcode and then climate zone"

    def formula(buildings, period, parameters):
        postcode = buildings('postcode', period)
        return parameters(period).energy_saving_scheme.test_output_cdd[postcode]  # This is a built in OpenFisca function that is used to calculate a single value for regional network factor based on a zipcode provided


class f_base_building(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "factor for base building NABERS calculation"

    def formula(buildings, period, parameters):
        adjusted_hours = buildings('maximum_nabers_adjusted_hours', period)
        return (1 / (0.38 + 0.0116 * adjusted_hours))


class f_tenancy(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "factor for tenancy NABERS calculation"

    def formula(buildings, period, parameters):
        adjusted_hours = buildings('maximum_nabers_adjusted_hours', period)
        return (1 / (0.38 + 0.0105 * adjusted_hours))


class SGEgas(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'specific greenhouse emissions for gas for the relevant state'

    def formula(buildings, period, parameters):
        state = buildings('building_state_location', period)
        return select(
            [state == "ACT", state == "NSW", state == "NT", state == 'SA',
             state == "QLD", state == "TAS", state == "VIC", state == "WA"],
            [0.23, 0.23, 0.20, 0.20, 0.21, 0.75, 0.21, 0.22]  # need to check these numbers, don't think they're right
            )

class SGEelec(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'specific greenhouse emissions for electricity for the relevant state'

    def formula(buildings, period, parameters):
        state = buildings('building_state_location', period)
        return select(
            [state == "ACT", state == "NSW", state == "NT", state == "QLD", state == "SA", state == "TAS", state == "VIC", state == "WA"],
            [0.94, 0.94, 0.69, 1.02, 0.95, 1, 1.34, 0.92]
            )


class SGEcoal (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'specific greenhouse emissions for coal for the relevant state'

    def formula(buildings, period, parameters):
        state = buildings('building_state_location', period)
        return select(
            [state == "ACT", state == "NSW", state == "NT", state == "QLD", state == "SA", state == "TAS", state == "VIC", state == "WA"],
            [0.32, 0.32, 0.32, 0.32, 0.32, 0.7, 0.32, 0.32]
            )


class SGEoil (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'specific greenhouse emissions for oil for the relevant state'

    def formula(buildings, period, parameters):
        state = buildings('building_state_location', period)
        return select(
            [state == "ACT", state == "NSW", state == "NT", state == "QLD", state == 'SA', state == "TAS", state == "VIC", state == "WA"],
            [0.27, 0.27, 0.27, 0.27, 0.27, 0.75, 0.27, 0.27]
            )


class SGEtenancy (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'specific greenhouse emissions for tenancy'

    def formula(buildings, period, parameters):
        SGEelec = buildings('SGEelec', period)
        return SGEelec


class term_1 (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Term 1used in the calculation of GEclimcorr"

    def formula(buildings, period, parameters):
        SGEgas = buildings('SGEgas', period)
        return np.round((4.12 * SGEgas), 4)


class term_2 (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Term 2 used in the calculation of GEclimcorr"

    def formula(buildings, period, parameters):
        SGEelec = buildings('SGEelec', period)
        return 43.6 * SGEelec


class term_3 (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Term 3 used in the calculation of GEclimcorr"

    def formula(buildings, period, parameters):
        SGEgas = buildings('SGEgas', period)
        HDD = buildings('HDD_18', period)
        return (0.0016 * SGEgas * HDD / 0.23)


class term_4 (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Term 4 used in the calculation of GEclimcorr"

    def formula(buildings, period, parameters):
        SGEelec = buildings('SGEelec', period)
        CDD15wb = buildings('CDD_15', period)
        return (0.091 * SGEelec * (CDD15wb / 0.94))  # 0.94 is likely SGEelec but need to check


class term_5 (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Term5 used in calculating GEclimcorr"

    def formula(buildings, period, parameters):
        SGEelec = buildings('SGEelec', period)
        CDD15wb = buildings('CDD_15', period)
        term_5_working = (0.062 * SGEelec * (CDD15wb - 400) / 0.94)  # 0.94 is likely SGEelec but need to check
        condition_term_5 = term_5_working >= 0
        return where(condition_term_5, term_5_working, 0)


class SGE_tenancy(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Specific greenhouse emissions related to tenancy of a building"

    def formula(buildings, period, parameters):
        return buildings('SGEelec', period)  # want to show that SGE_tenancy and SGEgas, while being identical values, are distinct parts of formulas within the calc


class Dequip (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Dequip value used to weigh impact of number of computers"

    def formula(buildings, period, parameters):
        return np.round(buildings('number_of_computers', period) * 0.20 / buildings('net_lettable_area', period), 8)


class GEclimcorr (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "climate corrected greenhouse emissions for the relevant NABERS whole building"  # check this

    def formula(buildings, period, parameters):
        Term1 = buildings('term_1', period)
        Term2 = buildings('term_2', period)
        Term3 = buildings('term_3', period)
        Term4 = buildings('term_4', period)
        Term5 = buildings('term_5', period)
        return Term1 + Term2 - Term3 - Term4 + Term5


class GEClimcorr_tenancy (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "weighted tenancy climate correct greenhouse emissions for the relevant NABERS building"

    def formula(buildings, period, parameters):
        return (4000 * buildings('SGE_tenancy', period) * (0.008 - buildings('Dequip', period)))


class coefficient_A(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "Rating equation coefficient_A used to calculate NABERS whole building ratings"

    def formula(buildings, period, parameters):
        state = buildings('building_state_location', period)
        rating_type = buildings('rating_type', period)
        return select(
            [state == "ACT" and rating_type == "whole_building"
            , state == "ACT" and rating_type == "tenancy"
            , state == "ACT" and rating_type == "base_building"
            , state == "NSW" and rating_type == "whole_building"
            , state == "NSW" and rating_type == "tenancy"
            , state == "NSW" and rating_type == "base_building"
            , state == "NT" and rating_type == "whole_building"
            , state == "NT" and rating_type == "tenancy"
            , state == "NT" and rating_type == "base_building"
            , state == "QLD" and rating_type == "whole_building"
            , state == "QLD" and rating_type == "tenancy"
            , state == "QLD" and rating_type == "base_building"
            , state == "SA" and rating_type == "whole_building"
            , state == "SA" and rating_type == "tenancy"
            , state == "SA" and rating_type == "base_building"
            , state == "TAS" and rating_type == "whole_building"
            , state == "TAS" and rating_type == "tenancy"
            , state == "TAS" and rating_type == "base_building"
            , state == "VIC" and rating_type == "whole_building"
            , state == "VIC" and rating_type == "tenancy"
            , state == "VIC" and rating_type == "base_building"
            , state == "WA" and rating_type == "whole_building"
            , state == "WA" and rating_type == "tenancy"
            , state == "WA" and rating_type == "base_building"
            ],
            [6.7605, 6.7727, 6.75, 6.7605, 6.7727, 6.75,
			 6.422206, 6.413814, 6.42932, 7.1, 6.2667, 8.35,
			 6.5247, 6.2636, 6.75, 6.5351, 6.2636, 6.75,
			 7.0114, 7.5889, 6.7544, 7.2857, 6.85, 7.6818]
            )


class coefficient_B(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "Rating equation coefficient_B used to calculate NABERS whole building ratings"

    def formula(buildings, period, parameters):
        state = buildings('building_state_location', period)
        rating_type = buildings('rating_type', period)
        return select(
            [state == "ACT" and rating_type == "whole_building"
            , state == "ACT" and rating_type == "tenancy"
            , state == "ACT" and rating_type == "base_building"
            , state == "NSW" and rating_type == "whole_building"
            , state == "NSW" and rating_type == "tenancy"
            , state == "NSW" and rating_type == "base_building"
            , state == "NT" and rating_type == "whole_building"
            , state == "NT" and rating_type == "tenancy"
            , state == "NT" and rating_type == "base_building"
            , state == "QLD" and rating_type == "whole_building"
            , state == "QLD" and rating_type == "tenancy"
            , state == "QLD" and rating_type == "base_building"
            , state == "SA" and rating_type == "whole_building"
            , state == "SA" and rating_type == "tenancy"
            , state == "SA" and rating_type == "base_building"
            , state == "TAS" and rating_type == "whole_building"
            , state == "TAS" and rating_type == "tenancy"
            , state == "TAS" and rating_type == "base_building"
            , state == "VIC" and rating_type == "whole_building"
            , state == "VIC" and rating_type == "tenancy"
            , state == "VIC" and rating_type == "base_building"
            , state == "WA" and rating_type == "whole_building"
            , state == "WA" and rating_type == "tenancy"
            , state == "WA" and rating_type == "base_building"
            ],
            [-0.0168067, -0.036364, -0.03125, -0.0168067, -0.036364, -0.03125,
			 -0.03323, -0.07242, -0.0614, -0.02, -0.0333, -0.05,
			 -0.0166656, -0.0359809, -0.0310451, -0.0151039, -0.0341818, -0.0270617,
			 -0.0148, -0.0444444, -0.0223, -0.02381, -0.05, -0.04545]
            )
