# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class YearsOfForwardCreation(Enum):
    one_year = u"User intends to forward create for one year."
    two_years = u"User intends to forward create for two years."
    three_years = u"User intends to forward create for three years."


class input_years_of_forward_creation(Variable):
    value_type = Enum
    possible_values = YearsOfForwardCreation
    default_value = YearsOfForwardCreation.one_year
    entity = Building
    definition_period = ETERNITY
    label = 'pulls the user input for the amount of years to be forward created' \
            ' within Step 5 through the enumerable.' \
            ' maximum allowable number of forward created years is 3.' \
            ' In accordance with clause 8.8.10 (a).'


class years_of_forward_creation(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Tests if a rating has been used for a previous Historical Baseline' \
            ' NABERS Rating for a NABERS Building. Clause 8.8.10 (c) prohibits' \
            ' the use of using a NABERS Rating of the same value more than once' \
            ' to set a fixed Historical NABERS Baseline Rating.'

    def formula(buildings, period, parameters):
        type_of_energy_savings = buildings('energy_savings_type', period)
        TypeOfEnergySavings = type_of_energy_savings.possible_values
        annual_creation = (type_of_energy_savings == TypeOfEnergySavings.annual_creation)
        forward_creation = (type_of_energy_savings == TypeOfEnergySavings.forward_creation)
        one_year_forward_creation = YearsOfForwardCreation.one_year
        two_years_forward_creation = YearsOfForwardCreation.two_years
        three_years_forward_creation = YearsOfForwardCreation.three_years
        return select([annual_creation
        , (one_year_forward_creation and forward_creation)
        , two_years_forward_creation and forward_creation
        , three_years_forward_creation and forward_creation],
        [1
        ,1
        ,2
        ,3])

class historical_rating_previously_used(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Tests if a rating has been used for a previous Historical Baseline' \
            ' NABERS Rating for a NABERS Building. Clause 8.8.10 (c) prohibits' \
            ' the use of using a NABERS Rating of the same value more than once' \
            ' to set a fixed Historical NABERS Baseline Rating.'

    def formula(buildings, period, parameters):
        condition_hist_rating_previously_used = buildings('historical_rating_previously_used_for_forward_creation', period)
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
    label = "value of year 1 of forward created electricity savings in MWh"

    def formula(buildings, period, parameters):
        benchmark_elec_consumption = buildings('benchmark_elec_consumption_MWh', period)
        measured_electricity_consumption = buildings('measured_electricity_consumption', period)
        regional_network_factor = buildings('regional_network_factor', period)
        forward_created_electricity_savings = (benchmark_elec_consumption
        - measured_electricity_consumption) * regional_network_factor
        return forward_created_electricity_savings


class year_two_forward_created_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "value of year 2 of forward created electricity savings"

    def formula(buildings, period, parameters):
        benchmark_elec_consumption = buildings('benchmark_elec_consumption_MWh', period)
        measured_electricity_consumption = buildings('measured_electricity_consumption', period)
        regional_network_factor = buildings('regional_network_factor', period)
        forward_created_electricity_savings = (benchmark_elec_consumption
        - measured_electricity_consumption) * regional_network_factor
        return forward_created_electricity_savings


class year_three_forward_created_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "value of year 3 of forward created electricity savings"

    def formula(buildings, period, parameters):
        benchmark_elec_consumption = buildings('benchmark_elec_consumption_MWh', period)
        measured_electricity_consumption = buildings('measured_electricity_consumption', period)
        regional_network_factor = buildings('regional_network_factor', period)
        forward_created_electricity_savings = (benchmark_elec_consumption
        - measured_electricity_consumption) * regional_network_factor
        return forward_created_electricity_savings


class year_one_forward_created_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "value of year 1 of forward created gas savings"

    def formula(buildings, period, parameters):
        benchmark_gas_consumption_MJ = buildings('benchmark_gas_consumption_MJ', period)
        measured_gas_consumption = buildings('measured_gas_consumption', period)
        gas_savings = benchmark_gas_consumption_MJ - measured_gas_consumption
        return gas_savings / 3.6


class year_two_forward_created_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "value of year 2 of forward created gas savings"

    def formula(buildings, period, parameters):
        benchmark_gas_consumption_MJ = buildings('benchmark_gas_consumption_MJ', period)
        measured_gas_consumption = buildings('measured_gas_consumption', period)
        gas_savings = benchmark_gas_consumption_MJ - measured_gas_consumption
        return gas_savings / 3.6

class year_three_forward_created_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "value of year 3 of forward created gas savings"

    def formula(buildings, period, parameters):
        benchmark_gas_consumption_MJ = buildings('benchmark_gas_consumption_MJ', period)
        measured_gas_consumption = buildings('measured_gas_consumption', period)
        gas_savings = benchmark_gas_consumption_MJ - measured_gas_consumption
        return gas_savings / 3.6


class total_forward_created_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "sum of total forward created electricity savings"

    def formula(buildings, period, parameters):
        years_of_forward_creation = buildings('years_of_forward_creation', period)
        year_one_elec_savings = buildings('year_one_forward_created_electricity_savings', period)
        year_two_elec_savings = buildings('year_two_forward_created_electricity_savings', period)
        year_three_elec_savings = buildings('year_three_forward_created_electricity_savings', period)

        return select(
            [years_of_forward_creation == 1
            , years_of_forward_creation == 2
            , years_of_forward_creation == 3],
            [year_one_elec_savings
            ,year_one_elec_savings + year_two_elec_savings
            ,year_one_elec_savings + year_two_elec_savings + year_three_elec_savings
            ]
            )


class total_forward_created_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "sum of total forward created gas savings"

    def formula(buildings, period, parameters):
        years_of_forward_creation = buildings('years_of_forward_creation', period)
        year_one_gas_savings = buildings('year_one_forward_created_gas_savings', period)
        year_two_gas_savings = buildings('year_two_forward_created_gas_savings', period)
        year_three_gas_savings = buildings('year_three_forward_created_gas_savings', period)

        return select(
            [years_of_forward_creation == 'one_year'
            , years_of_forward_creation == 'two_years'
            , years_of_forward_creation == 'three_years'],
            [year_one_gas_savings
            ,year_one_gas_savings + year_two_gas_savings
            ,year_one_gas_savings + year_two_gas_savings + year_three_gas_savings
            ]
            )
