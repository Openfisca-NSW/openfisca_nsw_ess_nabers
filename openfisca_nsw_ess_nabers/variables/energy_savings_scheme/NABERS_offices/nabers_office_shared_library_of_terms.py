# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *
import numpy as np
from openfisca_nsw_ess_nabers.variables.energy_savings_scheme.general_ESS.hidden_figures import get_parameters

private = True
if private:
    from openfisca_nsw_ess_nabers.variables.energy_savings_scheme.NABERS_offices import coefficient_values as c
else:
    from openfisca_nsw_ess_nabers.variables.energy_savings_scheme.NABERS_offices import public_coefficient_values as c

if not(c.has_real_values):
    error = ("real coefficients aren't used, and return values will be incorrect")

float_formatter = "{:.9f}".format
np.set_printoptions(formatter={'float_kind': float_formatter})

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
        return get_parameters(private, parameters(period).energy_savings_scheme.NABERS_offices,
                "climate_zones")[postcode]


class HDD_18(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'HDD value for the relevant climate zone, determined by the' \
            ' the relevant postcode.'

    def formula(buildings, period, parameters):
        postcode = buildings('postcode', period)
        return parameters(period).energy_savings_scheme.NABERS_offices.hdd[postcode]  # This is a built in OpenFisca function that is used to calculate a single value for regional network factor based on a zipcode provided


class CDD_15(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "The relevant cooling days for this building, based on postcode and then climate zone"

    def formula(buildings, period, parameters):
        postcode = buildings('postcode', period)
        return parameters(period).energy_savings_scheme.NABERS_offices.cdd[postcode]  # This is a built in OpenFisca function that is used to calculate a single value for regional network factor based on a zipcode provided


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
        return np.vectorize(c.SGE_coefficients.get)(state + "_SGE_gas")


class SGEelec(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'specific greenhouse emissions for electricity for the relevant state'

    def formula(buildings, period, parameters):
        state = buildings('building_state_location', period)
        return np.vectorize(c.SGE_coefficients.get)(state + "_SGE_elec")


class SGEcoal (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'specific greenhouse emissions for coal for the relevant state'

    def formula(buildings, period, parameters):
        state = buildings('building_state_location', period)
        return np.vectorize(c.SGE_coefficients.get)(state + "_SGE_coal")


class SGEoil (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'specific greenhouse emissions for oil for the relevant state'

    def formula(buildings, period, parameters):
        state = buildings('building_state_location', period)
        return np.vectorize(c.SGE_coefficients.get)(state + "_SGE_oil")


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
        return (4.12 * SGEgas)


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
        return buildings('number_of_computers', period) * 0.20 / buildings('net_lettable_area', period)


class GEclimcorr (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'climate corrected greenhouse emissions for the relevant' \
            ' NABERS whole building.'

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
    label = 'weighted tenancy climate correct greenhouse emissions for the' \
            ' relevant NABERS building.'

    def formula(buildings, period, parameters):
        return (4000 * buildings('SGE_tenancy', period) * (0.008 - buildings('Dequip', period)))


class coefficient_A(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = 'Rating equation coefficient_A used to calculate NABERS whole' \
            ' building ratings.'

    def formula(buildings, period, parameters):
        state = buildings('building_state_location', period)
        rating_type = buildings('rating_type', period)
        return np.vectorize(c.coefficient_A.get)(state + "_" + rating_type)


class coefficient_B(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = 'Rating equation coefficient_B used to calculate NABERS whole' \
            ' building ratings.'

    def formula(buildings, period, parameters):
        state = buildings('building_state_location', period)
        rating_type = buildings('rating_type', period)
        return np.vectorize(c.coefficient_B.get)(state + "_" + rating_type)


class NGEmax (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Normalised greenhouse emissions for relevant NABERS whole' \
            'building - only applicable under 5 stars'

    def formula(buildings, period, parameters):
        A = buildings('coefficient_A', period)
        B = buildings('coefficient_B', period)
        return ((buildings('benchmark_star_rating', period) - 0.499999 - A) / B)


class base_building_GEmax (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "GEmax value for base building ratings."

    def formula(buildings, period, parameters):
        NGEmax = buildings('NGEmax', period)
        f_base_building = buildings('f_base_building', period)
        GEclimcorr = buildings('GEclimcorr', period)
        return (NGEmax / f_base_building - GEclimcorr)


class tenancy_GEmax (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "GEmax value for tenancy ratings."

    def formula(buildings, period, parameters):
        NGEmax = buildings('NGEmax', period)
        f_tenancy = buildings('f_tenancy', period)
        GEClimcorr_tenancy = buildings('GEClimcorr_tenancy', period)
        return (NGEmax / f_tenancy - GEClimcorr_tenancy)


class GEwholemax (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Greenhouse emissions for relevant NABERS whole building' \
            ' - applicable above 5 stars.'

    def formula(buildings, period, parameters):
        condition_GEwholemax_star_rating = buildings('benchmark_star_rating', period) > 5
        return where(condition_GEwholemax_star_rating, 0,
                    (buildings('NGEmax', period) -
                     buildings('f_base_building', period) *
                     buildings('GEclimcorr', period) -
                     buildings('f_tenancy', period) *
                     buildings('GEClimcorr_tenancy', period)) * 2 /
                    (buildings('f_base_building', period) +
                        buildings('f_tenancy', period)))


class NGE_5star_original_rating (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "original normalised greenhouse emissions at 5 star for use for > 5 star ratings"

    def formula(buildings, period, parameters):
        A = buildings('coefficient_A', period)
        B = buildings('coefficient_B', period)
        return ((5 - A - 0.499999) / B)


class GE_5star_original_rating (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "original required maximum greenhouse emissions at 5 star rating"

    def formula(buildings, period, parameters):
        state = buildings('building_state_location', period)
        NGE_rating = buildings('NGE_5star_original_rating', period)
        f_bb = buildings('f_base_building', period)
        GEclimcorr = buildings('GEclimcorr', period)
        f_ten = buildings('f_tenancy', period)
        GEClimcorr_ten = buildings('GEClimcorr_tenancy', period)
        rating_type = buildings('rating_type', period)
        return select(
            [rating_type == "base_building"
            , rating_type == "tenancy"
            , rating_type == "whole_building"],
            [NGE_rating / f_bb - GEclimcorr
            , NGE_rating / f_ten - GEClimcorr_ten
            , (NGE_rating - f_bb * GEclimcorr - f_ten * GEClimcorr_ten)
             * 2 / (f_bb+f_ten)]
            )


class GE_25_percent_reduction(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "25% reduction of required maximum greenhouse emissions for use in 5.5 star rating following original rating system"

    def formula(buildings, period, parameters):
        GE_5_stars = buildings('GE_5star_original_rating', period)
        return GE_5_stars * 0.75


class GE_50_percent_reduction(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "50% reduction of required maximum greenhouse emissions for use in 6 star rating following original rating system"

    def formula(buildings, period, parameters):
        GE_5_stars = buildings('GE_5star_original_rating', period)
        return GE_5_stars * 0.5


class office_maximum_electricity_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "output of the NABERS whole building reverse calculator - the maximum electricity consumption allowable for the relevant NABERS rated building"  # need to figure out how to round this to an integer

    def formula(buildings, period, parameters):
        nla = buildings('net_lettable_area', period)
        benchmark = buildings('benchmark_star_rating', period)
        SGEelec = buildings('SGEelec', period)
        SGEgas = buildings('SGEgas', period)
        SGEcoal = buildings('SGEcoal', period)
        SGEoil = buildings('SGEoil', period)
        bb_GEmax = buildings('base_building_GEmax', period)
        ten_GEmax = buildings('tenancy_GEmax', period)
        GEwholemax = buildings('GEwholemax', period)
        GE_25_perc = buildings('GE_25_percent_reduction', period)
        GE_50_perc = buildings('GE_50_percent_reduction', period)
        perc_gas = buildings('perc_gas_kwh', period)
        perc_elec = buildings('perc_elec_kwh', period)
        perc_coal = buildings('perc_coal_kwh', period)
        perc_diesel = buildings('perc_diesel_kwh', period)
        rating_type = buildings('rating_type', period)

        def consumption(numerator):
            return np.round((numerator * nla) / (SGEelec +
            perc_gas / perc_elec * SGEgas +
            perc_coal / perc_elec * SGEcoal +
            perc_diesel / perc_elec * SGEoil), 9)

        return select(
            [(benchmark <= 5).any() and rating_type == "base_building"
            , (benchmark <= 5).any() and rating_type == "whole_building"
            , (benchmark <= 5).any() and rating_type == "tenancy"
            , (benchmark == 5.5).any() and rating_type == "whole_building"
            , (benchmark == 5.5).any() and rating_type == "base_building"
            , (benchmark == 5.5).any() and rating_type == "tenancy"
            , (benchmark == 6).any() and rating_type == "whole_building"
            , (benchmark == 6).any() and rating_type == "base_building"
            , (benchmark == 6).any() and rating_type == "tenancy"],
             [consumption(bb_GEmax)
             , consumption(GEwholemax)
             , consumption(ten_GEmax)
             , consumption(GE_25_perc)
             , consumption(GE_25_perc)
             , consumption(GE_25_perc)
             , consumption(GE_50_perc)
             , consumption(GE_50_perc)
             , consumption(GE_50_perc)])


class office_maximum_gas_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "output of the NABERS whole building reverse calculator - the maximum electricity consumption allowable for the relevant NABERS rated building"

    def formula(buildings, period, parameters):
        return (buildings('perc_gas_kwh', period) /
        buildings('perc_elec_kwh', period) *
        buildings('office_maximum_electricity_consumption', period) * 3.6)
