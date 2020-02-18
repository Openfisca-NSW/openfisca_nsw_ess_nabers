# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class years_of_forward_creation(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'defines the amount of years to be forward created within Step 5' \
            ' maximum allowable number of forward created years is 3.' \
            ' In accordance with clause 8.8.10 (a).'


class within_maximum_years_of_forward_creation(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Tests the distance between the end of the current rating period' \
            ' and the date of Energy Savings Certificates against the maximum' \
            ' allowable distance between end of rating and ESC creation date.' \
            ' In accordance with clause 8.8.10 (a).'

    def formula(buildings, period, parameters):
        return (
            buildings('years_of_forward_creation', period) <=
            parameters(period).energy_saving_scheme.preconditions.maximum_time_period_of_forward_creation
            )


class historical_rating_previously_used(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Tests if a rating has been used for a previous Historical Baseline' \
            ' NABERS Rating for a NABERS Building. Clause 8.8.10 (c) prohibits' \
            ' the use of using a NABERS Rating of the same value more than once' \
            ' to set a fixed Historical NABERS Baseline Rating.'

    def formula(buildings, period, parameters):
        condition_hist_rating_previously_used = buildings('historical_rating_previously_used_for_forward_creation', period) == True
        return where (condition_hist_rating_previously_used, False, True)


class historical_rating_previously_used_for_forward_creation(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks if a rating has been previously used to create a Historical' \
            ' Baseline NABERS Rating for the relevant NABERS building.'



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
            [years_of_forward_creation == 1, years_of_forward_creation == 2
            , years_of_forward_creation == 3],
            [year_one_forward_created_electricity_savings,
            year_one_forward_created_electricity_savings +
            year_two_forward_created_electricity_savings
            , year_one_forward_created_electricity_savings +
            year_two_forward_created_electricity_savings +
            year_three_forward_created_electricity_savings]
            )


class total_forward_created_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "sum of total forward created gas savings"

    def formula(buildings, period, parameters):
        return select(
            [years_of_forward_creation == 1
            , years_of_forward_creation == 2
            , years_of_forward_creation == 3],
            [year_one_forward_created_gas_savings
            , year_one_forward_created_gas_savings +
            year_two_forward_created_gas_savings
            , year_one_forward_created_gas_savings +
            year_two_forward_created_gas_savings +
            year_three_forward_created_gas_savings]
            )
