# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class measured_electricity_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "Measured Electricity Consumption (MWh)"

    def formula(buildings, period, parameters):
        return (buildings('nabers_electricity', period)
        + buildings('onsite_unaccounted_electricity', period))


class measured_gas_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "Measured Electricity Consumption (MWh)"

    def formula(buildings, period, parameters):
        return buildings('nabers_gas', period)


class nabers_electricity(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = 'NABERS Electricity, in MWh, is the electricity purchased or' \
            ' imported from the Electricity Network and accounted for in the' \
            ' NABERS Rating, including electricity purchased as GreenPower.'
            # Ilona, to how many decimal places should this be? Should there

    def formula(buildings, period, parameters):
        nabers_kWh = buildings('elec_kWh', period)
        return nabers_kWh / 1000

class onsite_unaccounted_electricity(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = 'On-site Unaccounted Electricity, in MWh, is electricity generated' \
            ' on-site from energy sources which have not been accounted for in' \
            ' the NABERS Rating, including electricity generated from' \
            ' photovoltaic cells or gas generators fed from on-site biogas' \
            ' sources, but excluding gas generators where the imported gas' \
            ' has been accounted for in the NABERS Rating.'


class nabers_gas(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = 'NABERS Gas, in MWh, is the total of the Gas accounted for in' \
            ' the NABERS rating'

    def formula(buildings, period, parameters):
        NABERS_gas_MJ = buildings('gas_in_MJ', period)
        return (NABERS_gas_MJ / 3.6) / 1000
        # Ilona, Andrew - is it better to have an implied MJ > kWh > MWh
        # conversion string, or simply go MJ > MWh (which would mean this
        # would be return (NABERS_gas_MJ / 3600)? Please advise (if this is)
        # important.
