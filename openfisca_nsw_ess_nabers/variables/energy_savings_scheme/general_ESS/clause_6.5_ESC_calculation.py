# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *
import numpy as np


class number_of_certificates(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The total number of certificates generated from this activity.' \


    def formula(buildings, period, parameters):
        elec_savings = buildings('electricity_savings', period)
        elec_cert_conversion_factor = parameters(period).energy_savings_scheme.electricity_certificate_conversion_factor
        gas_savings = buildings('gas_savings', period)
        gas_cert_conversion_factor = parameters(period).energy_savings_scheme.gas_certificate_conversion_factor
        eligible_to_create_ESCs = buildings('NABERS_eligible_to_create_ESCs', period)
        return np.floor(((elec_savings * elec_cert_conversion_factor) + (gas_savings * gas_cert_conversion_factor)) * eligible_to_create_ESCs)
