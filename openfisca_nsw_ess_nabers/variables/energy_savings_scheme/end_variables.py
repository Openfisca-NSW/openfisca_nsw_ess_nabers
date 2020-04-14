# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *



from preconditions import NABERS_eligible_to_create_ESCs # returning end eligibility criteria required to create ESCs - this function integrates all of the ESC eligibility requirements
from step_three import benchmark_elec_consumption
from step_three import benchmark_gas_consumption_MWh # returning benchmark elec and gas is required to demonstrate functionality of NABERS reverse calculators, this function returns benchmark of all building types
from step_three import electricity_savings # returning elec and gas savings is required within the ESS. note elec savings is benchmark_elec_consumption - measured_elec_consumption
from step_three import gas_savings # as above
from general_ess import number_of_certificates # total number of certificates is required to demonstrate potential of the ESS for NABERS users
