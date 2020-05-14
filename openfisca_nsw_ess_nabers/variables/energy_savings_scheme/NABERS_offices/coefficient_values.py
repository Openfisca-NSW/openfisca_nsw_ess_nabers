# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *
# from openfisca_nsw_ess_nabers.variables.energy_savings_scheme.NABERS_offices import nabers_office_shared_library_of_terms
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
                    "WA_SGE_gas": 0.22,
                    "ACT_SGE_elec": 0.94,
                    "NSW_SGE_elec": 0.94,
                    "NT_SGE_elec": 0.69,
                    "QLD_SGE_elec": 1.02,
                    "SA_SGE_elec": 0.95,
                    "TAS_SGE_elec": 1,
                    "VIC_SGE_elec": 1.34,
                    "WA_SGE_elec": 0.92,
                    "ACT_SGE_coal": 0.32,
                    "NSW_SGE_coal": 0.32,
                    "NT_SGE_coal": 0.32,
                    "QLD_SGE_coal": 0.32,
                    "SA_SGE_coal": 0.32,
                    "TAS_SGE_coal": 0.7,
                    "VIC_SGE_coal": 0.32,
                    "WA_SGE_coal": 0.32,
                    "ACT_SGE_oil": 0.27,
                    "NSW_SGE_oil": 0.27,
                    "NT_SGE_oil": 0.27,
                    "QLD_SGE_oil": 0.27,
                    "SA_SGE_oil": 0.27,
                    "TAS_SGE_oil": 0.75,
                    "VIC_SGE_oil": 0.27,
                    "WA_SGE_oil": 0.27
                    }


CDD_coefficients = {
                    "Climate_zone_64_value": 80,
                    }

coefficient_A = {
                    "ACT_whole_building": 6.7605,
                    "ACT_base_building": 6.75,
                    "ACT_tenancy": 6.7727,
                    "NSW_whole_building": 6.760,
                    "NSW_base_building": 6.75,
                    "NSW_tenancy": 6.7727,
                    "NT_whole_building": 6.422206,
                    "NT_base_building": 6.42932,
                    "NT_tenancy": 6.413814,
                    "QLD_whole_building": 7.1,
                    "QLD_base_building": 8.35,
                    "QLD_tenancy": 6.2667,
                    "SA_whole_building": 6.5247,
                    "SA_base_building": 6.75,
                    "SA_tenancy": 6.2636,
                    "TAS_whole_building": 6.5351,
                    "TAS_base_building": 6.75,
                    "TAS_tenancy": 6.2636,
                    "VIC_whole_building": 7.0114,
                    "VIC_base_building": 6.7544,
                    "VIC_tenancy": 7.5889,
                    "WA_whole_building": 7.2857,
                    "WA_base_building": 7.6818,
                    "WA_tenancy": 6.85,
                    }

coefficient_B = {
                    "ACT_whole_building": -0.0168067,
                    "ACT_base_building": -0.03125,
                    "ACT_tenancy": -0.036364,
                    "NSW_whole_building": -0.0168067,
                    "NSW_base_building": -0.03125,
                    "NSW_tenancy": -0.036364,
                    "NT_whole_building": -0.03323,
                    "NT_base_building": -0.0614,
                    "NT_tenancy": -0.07242,
                    "QLD_whole_building": -0.02,
                    "QLD_base_building": -0.05,
                    "QLD_tenancy": -0.0333,
                    "SA_whole_building": -0.0166656,
                    "SA_base_building": -0.0310451,
                    "SA_tenancy": -0.0359809,
                    "TAS_whole_building": -0.0151039,
                    "TAS_base_building": -0.0270617,
                    "TAS_tenancy": -0.0341818,
                    "VIC_whole_building": -0.0148,
                    "VIC_base_building": -0.0223,
                    "VIC_tenancy": -0.0444444,
                    "WA_whole_building": -0.02381,
                    "WA_base_building": -0.04545,
                    "WA_tenancy": -0.05,
                    }


def has_real_values():
    return True
