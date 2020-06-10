# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class annually_created_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "What is the electricity savings in MWh?"

    def formula(buildings, period, parameters):
        benchmark_elec_consumption = buildings('benchmark_elec_consumption_MWh', period)
        measured_electricity_consumption = buildings('measured_electricity_consumption', period)
        counted_elec_savings = buildings('counted_elec_savings', period)
        regional_network_factor = buildings('regional_network_factor', period)
        previous_year_elec_savings = buildings('electricity_savings_previous_year', period)
        electricity_savings = ((benchmark_elec_consumption
        - measured_electricity_consumption)
        * regional_network_factor
        - counted_elec_savings + previous_year_elec_savings)
        return electricity_savings  # Year based calculations are missing from this formula. Need to be added


class annually_created_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "What is the gas savings in MWh?"

    def formula(buildings, period, parameters):
        benchmark_gas_consumption_MWh = buildings('benchmark_gas_consumption_MWh', period)
        measured_gas_consumption = buildings('measured_gas_consumption', period)
        counted_gas_savings = buildings('counted_gas_savings', period)
        previous_year_gas_savings = buildings('gas_savings_previous_year', period)
        gas_savings = (benchmark_gas_consumption_MWh - measured_gas_consumption
        - counted_gas_savings + previous_year_gas_savings)
        return gas_savings  # Year based calculations are missing from this formula. Need to be added


class regional_network_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor is the value from Table A24 of Schedule' \
            ' A corresponding to the postcode of the Address of the Site or' \
            ' Sites where the Implementation(s) took place.'

    def formula(buildings, period, parameters):
        postcode = buildings('postcode', period)
        rnf = parameters(period).energy_savings_scheme.table_a24.regional_network_factor
        return rnf.calc(postcode)  # This is a built in OpenFisca function that \
        # is used to calculate a single value for regional network factor based on a zipcode provided


class NRYi1(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'the NABERS rating year immediately preceding the NABERS Rating' \
            ' Year.'
    # note this only says "NABERS Rating Year in the rule -
    # you need to define this as current rating year."

    def formula(buildings, period, parameters):
        current_rating_year = buildings('current_rating_year', period)
        return current_rating_year - 1


class counted_elec_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Total Elec Savings for which Energy Savings Certificates have' \
            'previously been created for the Implementation for the Current' \
            'Rating Year in MWh'


class electricity_savings_previous_year(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the electricity savings created for the year NRYi-1 - the' \
            ' previous NABERS Rating Year?'


class counted_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the total Gas Savings for which Energy Savings' \
            ' Certificates have previously been created for the Implementation' \
            ' for the Current Rating Year in MWh?'


class gas_savings_previous_year(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the gas savings created for the year NRYi-1 - the' \
            ' previous NABERS Rating Year?'


class counted_energy_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The total Energy Savings for which ESCs have previously been' \
            ' created for the Implementation for the Current Rating Year.' \
            ' As defined in Clause 8.8.12.'

    """
    def formula(buildings, period, parameters):
        cg_savings = buildings('counted_gas_savings', period)
        ce_savings = buildings('counted_elec_savings', period)
        return count_elec_savings + count_gas_savings
    """
