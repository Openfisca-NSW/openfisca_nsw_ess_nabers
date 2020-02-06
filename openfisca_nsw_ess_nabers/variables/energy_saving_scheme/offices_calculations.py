# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *
import numpy as np
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
    label = "Greenhouse emissions for relevant NABERS whole building - applicable above 5 stars"

    def formula(buildings, period, parameters):
        condition_GEwholemax_star_rating = buildings('benchmark_star_rating', period) > 5
        return where(condition_GEwholemax_star_rating, 0, (buildings('NGEmax', period) - buildings('f_base_building', period) * buildings('GEclimcorr', period) - buildings('f_tenancy', period) * buildings('GEClimcorr_tenancy', period)) * 2 / (buildings('f_base_building', period) + buildings('f_tenancy', period)))


class NGE_5star_original_rating (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "original normalised greenhouse emissions at 5 star for use for > 5 star ratings"

    def formula(buildings, period, parameters):
        A = buildings('coefficient_A', period)
        B = buildings('coefficient_B', period)
        return np.round(((5 - A - 0.499999) / B), 7)


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
        return np.round(select(
            [rating_type == "base_building"
            , rating_type == "tenancy"
            , rating_type == "whole_building"],
            [NGE_rating / f_bb - GEclimcorr
            , NGE_rating / f_ten - GEClimcorr_ten
            , (NGE_rating - f_bb * GEclimcorr - f_ten * GEClimcorr_ten)
             * 2 / (f_bb+f_ten)]
            ), 6)

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
        return select(
            [benchmark <= 5 and rating_type == "whole_building"
            , benchmark <= 5 and rating_type == "base_building"
            , benchmark <= 5 and rating_type == "tenancy"
            , benchmark == 5.5 and rating_type == "whole_building"
            , benchmark == 5.5 and rating_type == "base_building"
            , benchmark == 5.5 and rating_type == "tenancy"
            , benchmark == 6 and rating_type == "whole_building"
            , benchmark == 6 and rating_type == "base_building"
            , benchmark == 6 and rating_type == "tenancy"],
            [(GEwholemax * nla) / (SGEelec + perc_gas / perc_elec * SGEgas + perc_coal / perc_elec * SGEcoal + perc_diesel / perc_elec * SGEoil)
             , (bb_GEmax * nla) / (SGEelec + perc_gas / perc_elec * SGEgas + perc_coal / perc_elec * SGEcoal + perc_diesel / perc_elec * SGEoil)
             , (ten_GEmax * nla) / (SGEelec + perc_gas / perc_elec * SGEgas + perc_coal / perc_elec * SGEcoal + perc_diesel / perc_elec * SGEoil)
             , (GE_25_perc * nla) / (SGEelec + perc_gas / perc_elec * SGEgas + perc_coal / perc_elec * SGEcoal + perc_diesel / perc_elec * SGEoil)
             , (GE_25_perc * nla) / (SGEelec + perc_gas / perc_elec * SGEgas + perc_coal / perc_elec * SGEcoal + perc_diesel / perc_elec * SGEoil)
             , (GE_25_perc * nla) / (SGEelec + perc_gas / perc_elec * SGEgas + perc_coal / perc_elec * SGEcoal + perc_diesel / perc_elec * SGEoil)
             , (GE_50_perc * nla) / (SGEelec + perc_gas / perc_elec * SGEgas + perc_coal / perc_elec * SGEcoal + perc_diesel / perc_elec * SGEoil)
             , (GE_50_perc * nla) / (SGEelec + perc_gas / perc_elec * SGEgas + perc_coal / perc_elec * SGEcoal + perc_diesel / perc_elec * SGEoil)
             , (GE_50_perc * nla) / (SGEelec + perc_gas / perc_elec * SGEgas + perc_coal / perc_elec * SGEcoal + perc_diesel / perc_elec * SGEoil)]
            )


class office_maximum_gas_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "output of the NABERS whole building reverse calculator - the maximum electricity consumption allowable for the relevant NABERS rated building"

    def formula(buildings, period, parameters):
        return (buildings('perc_gas_kwh', period) / buildings('perc_elec_kwh', period) * buildings('office_maximum_electricity_consumption', period) * 3.6)
