# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class hours_per_week_with_20_percent_occupancy(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Hours each week with occupancy levels of 20% or more (hrs/week)"


class net_lettable_area(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "The net lettable area of the building"


class building_area_type(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'The area/type of the building for which the calculation is being' \
            ' processed (For example: base building, whole building, tenancy,' \
            ' etc)'


class apartments_benchmark_elec_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = 'Condition that determines where end result of the Apartments' \
            ' Reverse Calculator is to be used as the Benchmark Energy' \
            ' Value.'

    def formula(buildings, period, parameters):
        condition_apartment_benchmark = buildings('is_apartment_building', period) == True
        return where (condition_apartment_benchmark,
        buildings('predicted_electricity_kWh', period), 0)


class apartments_benchmark_gas_consumption_MJ(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = 'Condition that determines where end result of the Apartments' \
            ' Reverse Calculator is to be used as the Benchmark Energy' \
            ' Value.'

    def formula(buildings, period, parameters):
        condition_apartment_benchmark = buildings('is_apartment_building', period) == True
        return where (condition_apartment_benchmark,
        buildings('predicted_gas_MJ', period), 0)


class offices_benchmark_elec_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "Benchmark electricity consumption amount obtained from NABERS reverse calculator"

    def formula(buildings, period, parameters):
        condition_office_benchmark = buildings('is_office', period) == True
        return where (condition_office_benchmark,
        buildings('office_maximum_electricity_consumption', period), 0)


class offices_benchmark_gas_consumption_MJ(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "Benchmark electricity consumption amount obtained from NABERS reverse calculator"

    def formula(buildings, period, parameters):
        condition_office_benchmark = buildings('is_office', period) == True
        return where (condition_office_benchmark,
        buildings('office_maximum_gas_consumption', period), 0)


class benchmark_elec_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "Benchmark electricity consumption amount obtained from NABERS reverse calculator"

    def formula(buildings, period, parameters):
        return select([buildings('is_office', period),
        buildings('is_apartment_building', period)],
        [buildings('offices_benchmark_elec_consumption', period),
        buildings('apartments_benchmark_elec_consumption', period)]
            )


class benchmark_elec_consumption_MWh(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = 'Benchmark electricity consumption in mWh, as required by Step 3' \
            ' of ESS NABERS Method.'

    def formula(buildings, period, parameters):
        return buildings('benchmark_elec_consumption', period) / 1000


class benchmark_gas_consumption_MJ(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "Benchmark gas consumption amount obtained from NABERS reverse calculator"

    def formula(buildings, period, parameters):
        return select([buildings('is_apartment_building', period),
        buildings('is_office', period)],
        [buildings('apartments_benchmark_gas_consumption_MJ', period),
        buildings('office_maximum_gas_consumption', period)]
            )

class benchmark_gas_consumption_MWh(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "Benchmark gas consumption amount obtained from NABERS reverse calculator"

    def formula(buildings, period, parameters):
        gas_MJ = buildings('benchmark_gas_consumption_MJ', period)
        return gas_MJ / 3600


class TypeOfEnergySavings(Enum):
    annual_creation = u'Energy Savings are annually created and uses step 4 to' \
                      ' calculate Energy Savings'
    forward_creation = u'Energy Savings are forward created and uses step 5 to' \
                      ' calculate Energy Savings'


class energy_savings_type(Variable):
    value_type = Enum
    possible_values = TypeOfEnergySavings
    default_value = TypeOfEnergySavings.forward_creation
    entity = Building
    definition_period = ETERNITY
    label = u'Determines the type of energy savings created.'


class electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns electricity savings, for use in calculating the amount' \
            ' of certificates generated in this implementation.'

    def formula(buildings, period, parameters):
        type_of_energy_savings = buildings('energy_savings_type', period)
        annual_creation = (type_of_energy_savings == TypeOfEnergySavings.annual_creation)
        forward_creation = (type_of_energy_savings == TypeOfEnergySavings.forward_creation)
        annually_created_electricity_savings = buildings('annually_created_electricity_savings', period)
        forward_created_electricity_savings = buildings('total_forward_created_electricity_savings', period)
        return(annually_created_electricity_savings * annual_creation) + (forward_created_electricity_savings * forward_creation)

class gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns electricity savings, for use in calculating the amount' \
            ' of certificates generated in this implementation.'

    def formula(buildings, period, parameters):
        type_of_energy_savings = buildings('energy_savings_type', period)
        annual_creation = (type_of_energy_savings == TypeOfEnergySavings.annual_creation)
        forward_creation = (type_of_energy_savings == TypeOfEnergySavings.forward_creation)
        annually_created_gas_savings = buildings('annually_created_gas_savings', period)
        forward_created_gas_savings = buildings('total_forward_created_gas_savings', period)
        return(annually_created_gas_savings * annual_creation) + (forward_created_gas_savings * forward_creation)
