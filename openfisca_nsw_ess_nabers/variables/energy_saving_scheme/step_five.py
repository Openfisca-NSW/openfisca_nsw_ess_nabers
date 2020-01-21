# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class forward_creation_maximum_length(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "defines the length of forward creation process - maximum three years"

    def formula(buildings, period, parameters):
        condition_forward_creation = building('years_of_forward_creation', period) > 3
        return where(condition_forward_creation, 3 + "maximum number of years for forward creation is 3", 'years_of_forward_creation')


class year_one_forward_created_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "value of year 1 of forward created electricity savings"

    def formula(buildings, period, parameters):
        benchmark_elec_consumption = buildings('benchmark_elec_consumption', period)
        measured_electricity_consumption = buildings('measured_electricity_consumption', period)
        regional_network_factor = buildings('regional_network_factor', period)
        forward_created_electricity_savings = (benchmark_elec_consumption - measured_electricity_consumption) * regional_network_factor
        return forward_created_electricity_savings


class year_two_forward_created_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "value of year 2 of forward created electricity savings"

    def formula(buildings, period, parameters):
        benchmark_elec_consumption = buildings('benchmark_elec_consumption', period)
        measured_electricity_consumption = buildings('measured_electricity_consumption', period)
        regional_network_factor = buildings('regional_network_factor', period)
        forward_created_electricity_savings = (benchmark_elec_consumption - measured_electricity_consumption) * regional_network_factor
        return forward_created_electricity_savings


class year_three_forward_created_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "value of year 3 of forward created electricity savings"

    def formula(buildings, period, parameters):
        benchmark_elec_consumption = buildings('benchmark_elec_consumption', period)
        measured_electricity_consumption = buildings('measured_electricity_consumption', period)
        regional_network_factor = buildings('regional_network_factor', period)
        forward_created_electricity_savings = (benchmark_elec_consumption - measured_electricity_consumption) * regional_network_factor
        return forward_created_electricity_savings


class year_one_forward_created_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "value of year 1 of forward created gas savings"

    def formula(buildings, period, parameters):
        benchmark_gas_consumption = buildings('benchmark_gas_consumption', period)
        measured_gas_consumption = buildings('measured_gas_consumption', period)
        gas_savings = benchmark_gas_consumption - measured_gas_consumption
        return gas_savings  # Year based calculations are missing from this formula. Need to be added


class year_two_forward_created_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "value of year 2 of forward created gas savings"

    def formula(buildings, period, parameters):
        benchmark_gas_consumption = buildings('benchmark_gas_consumption', period)
        measured_gas_consumption = buildings('measured_gas_consumption', period)
        gas_savings = benchmark_gas_consumption - measured_gas_consumption
        return gas_savings  # Year based calculations are missing from this formula. Need to be added


class year_three_forward_created_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "value of year 3 of forward created gas savings"

    def formula(buildings, period, parameters):
        benchmark_gas_consumption = buildings('benchmark_gas_consumption', period)
        measured_gas_consumption = buildings('measured_gas_consumption', period)
        gas_savings = benchmark_gas_consumption - measured_gas_consumption
        return gas_savings  # Year based calculations are missing from this formula. Need to be added


class total_forward_created_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "sum of total forward created electricity savings"

    def formula(buildings, period, parameters):
        return select(
            [years_of_forward_creation == 1, years_of_forward_creation == 2, years_of_forward_creation == 3],
            [year_one_forward_created_electricity_savings, year_one_forward_created_electricity_savings + year_two_forward_created_electricity_savings, year_one_forward_created_electricity_savings + year_two_forward_created_electricity_savings + year_three_forward_created_electricity_savings]
            )


class total_forward_created_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "sum of total forward created gas savings"

    def formula(buildings, period, parameters):
        return select(
            [years_of_forward_creation == 1, years_of_forward_creation == 2, years_of_forward_creation == 3],
            [year_one_forward_created_gas_savings, year_one_forward_created_gas_savings + year_two_forward_created_gas_savings, year_one_forward_created_gas_savings + year_two_forward_created_gas_savings + year_three_forward_created_gas_savings]
            )
