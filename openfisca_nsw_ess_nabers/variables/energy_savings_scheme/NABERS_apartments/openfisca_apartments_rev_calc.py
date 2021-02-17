# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

import numpy as np
float_formatter = "{:.9f}".format
np.set_printoptions(formatter={'float_kind': float_formatter})

# xlsx = r'/Users/liammccann/DPIE/Energy Savings Scheme - 02_Rule as Code/01_ESS/01. 8.8 NABERS/1. Data/climate_zones_postcodes.xlsx'
# df1 = pd.read_excel(xlsx, "postcodes")
# df2 = pd.read_excel(xlsx, "climate_zone")
# df1.index = df1.Postcode
# df2.index = df2.Climate_id
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

# postcode = 2042
#
# climate_zone_value = df1.loc[df1['Postcode'] == postcode, 'Climate_zone'].values[0]
# hdd = df2.loc[df2['Climate_id'] == climate_zone_value, 'Hdd'].values[0]
# cdd = df2.loc[df2['Climate_id'] == climate_zone_value, 'Cdd'].values[0]

# %% user inputs


class predicted_electricity_kWh(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the predicted electricity consumption of the relevant NABERS' \
            ' rated apartment building, in kWh? This is also known as the benchmark' \
            ' electricity consumption.'  # need to code in condition - if less than zero, = 0. Note that this is identical to the benchmark figure, and to the Maximum Energy Consumption within the offices calculator.


class predicted_gas_MJ(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the predicted gas consumption of the relevant NABERS' \
            ' rated apartment building, in MJ? This is also known as the benchmark' \
            ' gas consumption.'  # need to code in condition - if less than zero, = 0. Note that this is identical to the benchmark figure, and to the Maximum Energy Consumption within the offices calculator.
