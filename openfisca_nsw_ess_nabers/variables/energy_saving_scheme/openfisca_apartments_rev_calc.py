# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

from pandas import pandas as pd

xlsx = r'/Users/liammccann/DPIE/Energy Savings Scheme - 02_Rule as Code/01_ESS/01. 8.8 NABERS/1. Data/climate_zones_postcodes.xlsx'
df1 = pd.read_excel(xlsx, "postcodes")
df2 = pd.read_excel(xlsx, "climate_zone")
df1.index = df1.Postcode
df2.index = df2.Climate_id
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

postcode = 2042

climate_zone_value = df1.loc[df1['Postcode'] == postcode, 'Climate_zone'].values[0]
hdd = df2.loc[df2['Climate_id'] == climate_zone_value, 'Hdd'].values[0]
cdd = df2.loc[df2['Climate_id'] == climate_zone_value, 'Cdd'].values[0]

# %% user inputs


class number_of_apartments(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Number of apartments located in the NABERS rated apartment' \
            ' building.'


class number_of_central_ac_apartments(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Number of centrally air conditioned apartments located in the' \
            ' NABERS rated apartment building.'


class number_of_condenser_water_serviced_apartments(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Number of condenser water serviced apartments located in the' \
            ' NABERS rated apartment building.'


class pool_coefficient(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'pool coefficient used to indicate whether the complex has no' \
            ' pool, an unheated pool, or a heated pool.'  # note this is currently a numerical value, we should code this as a string


class gym_coefficient(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'gym boolean value used to indicate whether the complex has no' \
            ' gym or a gym.'  # note this is currently a numerical value, we should code this as a string


class number_of_naturally_ventilated_parking_spaces(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Number of naturally ventilated parking spaces located in the' \
            ' NABERS rated apartment building.'


class number_of_mechanically_ventilated_parking_spaces(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Number of mechanically ventilated parking spaces located in the' \
            ' NABERS rated apartment building.'


class central_AC(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Weighting of the central AC coefficient against the number of' \
            ' apartments with Central AC divided by the number of total' \
            ' apartments.'

    def formula(buildings, period, parameters):
        AC_coeff = parameters(period).energy_saving_scheme.NABERS_apartments.elec_coeff
        number_of_AC_apart = buildings('number_of_central_ac_apartments', period)
        number_of_apart = buildings('number_of_apartments', period)
        central_AC = ((number_of_AC_apart * AC_coeff) / number_of_apart)
        return central_AC


class car_park_variable(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Weighting of the number of mechanically ventilated carpark spaces' \
            ' against the mechanically ventilated coefficient, plus the' \
            ' number of naturally ventilated carpark spaces weighted against' \
            ' naturally ventilated carpark coefficient, divided by the total' \
            ' number of apartments.'

    def formula(buildings, period, parameters):
        mvcp_coeff = parameters(period).energy_saving_scheme.NABERS_apartments.mech_ventilated_carpark_coeff
        nvcp_coeff = parameters(period).energy_saving_scheme.NABERS_apartments.natural_ventilated_carpark_coeff
        no_mech_vent_parking_spaces = buildings('number_of_mechanically_ventilated_parking_spaces', period)
        no_nat_vent_parking_spaces = buildings('number_of_mechanically_ventilated_parking_spaces', period)
        number_of_apart = buildings('number_of_apartments', period)
        car_park = ((no_mech_vent_parking_spaces * mvcp_coeff) + (no_nat_vent_parking_spaces * nvcp_coeff * mvcp_coeff)) / number_of_apart
        return car_park
