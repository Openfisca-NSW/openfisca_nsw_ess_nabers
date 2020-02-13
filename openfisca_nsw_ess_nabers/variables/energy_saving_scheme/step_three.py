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
    label = "The area/type of the building for which the calculation is being processed (For example: base building, whole building, tenancy, etc)"


class apartments_benchmark_elec_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = 'Condition that determines where end result of the Apartments' \
            ' Reverse Calculator is to be used as the Benchmark Energy' \
            ' Value.'

    def formula(buildings, period, parameters):
        condition_apartment_benchmark = buildings('is_apartment_building', period) == True
        return where (condition_apartment_benchmark, buildings('predicted_electricity_kWh', period), 0)


class apartments_benchmark_gas_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = 'Condition that determines where end result of the Apartments' \
            ' Reverse Calculator is to be used as the Benchmark Energy' \
            ' Value.'

    def formula(buildings, period, parameters):
        condition_apartment_benchmark = buildings('is_apartment_building', period) == True
        return where (condition_apartment_benchmark, buildings('predicted_gas_MJ', period), 0)


class offices_benchmark_elec_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "Benchmark electricity consumption amount obtained from NABERS reverse calculator"

    def formula(buildings, period, parameters):
        condition_office_benchmark = buildings('is_office', period) == True
        return where (condition_office_benchmark, buildings('office_maximum_electricity_consumption', period), 0)


class offices_benchmark_gas_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "Benchmark electricity consumption amount obtained from NABERS reverse calculator"

    def formula(buildings, period, parameters):
        condition_office_benchmark = buildings('is_office', period) == True
        return where (condition_office_benchmark, buildings('office_maximum_gas_consumption', period), 0)


class benchmark_elec_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "Benchmark electricity consumption amount obtained from NABERS reverse calculator"

    def formula(buildings, period, parameters):
        return select([buildings('is_office', period), buildings('is_apartment_building', period)],
        [buildings('offices_benchmark_elec_consumption', period), buildings('apartments_benchmark_elec_consumption', period)]
            )


class benchmark_elec_consumption_mWh(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = 'Benchmark electricity consumption in mWh, as required by Step 3' \
            ' of ESS NABERS Method.'

    def formula(buildings, period, parameters):
        return buildings('benchmark_elec_consumption', period) / 1000


class benchmark_gas_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "Benchmark gas consumption amount obtained from NABERS reverse calculator"

    def formula(buildings, period, parameters):
        return select([buildings('is_office', period), buildings('is_apartment_building', period)],
        [buildings('office_maximum_gas_consumption', period), buildings('apartments_benchmark_gas_consumption', period)]
            )
