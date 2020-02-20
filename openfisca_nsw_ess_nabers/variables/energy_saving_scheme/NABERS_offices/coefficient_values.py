# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *
from openfisca_nsw_ess_nabers.variables.energy_saving_scheme.NABERS_offices import nabers_office_shared_library_of_terms
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

# note that this file is used to store variables which are IDENTICAL across
# NABERS office reverse calculators. This file is to be made PRIVATE.

SGE_coefficients = {
                    "ACT_SGE_gas": 0.23,
                    "NSW_SGE_gas": 0.23,
                    "NT_SGE_gas": 0.20,
                    "QLD_SGE_gas": 0.20,
                    "SA_SGE_gas": 0.21,
                    "TAS_SGE_gas": 0.75,
                    "VIC_SGE_gas": 0.21,
                    "WA_SGE_gas": 0.22
                    }


CDD_coefficients = {
                    "Climate_zone_64_value": 80,
                    }

def has_real_values():
    return True
