# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class is_office(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = "Building is an office"

    def formula(buildings, period, parameters):
        building_type = buildings('building_type_status', period)
        condition_is_office = (building_type == BuildingTypeStatus.office)
        return where(condition_is_office, 1, 0)


class is_hotel(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = "Building is a hotel"

    def formula(buildings, period, parameters):
        building_type = buildings('building_type_status', period)
        condition_is_hotel = (building_type == BuildingTypeStatus.hotel)
        return where(condition_is_hotel, 1, 0)


class is_shopping_centre(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = "Building is a shopping centre"

    def formula(buildings, period, parameters):
        building_type = buildings('building_type_status', period)
        condition_is_shopping_centre = (building_type == BuildingTypeStatus.shopping_centre)
        return where(condition_is_shopping_centre, 1, 0)


class is_data_centre(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = "Building is a data centre"

    def formula(buildings, period, parameters):
        building_type = buildings('building_type_status', period)
        condition_is_data_centre = (building_type == BuildingTypeStatus.data_centre)
        return where(condition_is_data_centre, 1, 0)


class is_hospital(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = "Building is a hospital"

    def formula(buildings, period, parameters):
        building_type = buildings('building_type_status', period)
        condition_is_hospital = (building_type == BuildingTypeStatus.hospital)
        return where(condition_is_hospital, 1, 0)


class is_apartment_building(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = "Building is an apartment building"

    def formula(buildings, period, parameters):
        building_type = buildings('building_type_status', period)
        condition_is_apartment_building = (building_type == BuildingTypeStatus.apartment_building)
        return where(condition_is_apartment_building, 1, 0)


class BuildingTypeStatus(Enum):
    apartment_building = u"NABERS rated building is an apartment building"
    data_centre = u"NABERS rated building is a data centre"
    hospital = u"NABERS rated building is a hospital"
    hotel = u"NABERS rated building is an hotel"
    office = u"NABERS rated building is an office"
    shopping_centre = u"NABERS rated building is a shopping centre"


class building_type_status(Variable):
    value_type = Enum
    possible_values = BuildingTypeStatus
    default_value = BuildingTypeStatus.apartment_building
    entity = Building
    definition_period = ETERNITY
    label = u'The building type of the NABERS rating building, as entered by' \
            ' the user.'


class building_type(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'What is the building type for which you are calculating ESCs?' \


    def formula(buildings, period, parameters):
        building_type = buildings('building_type_status', period)
        is_apartment_building = (building_type == BuildingTypeStatus.apartment_building)
        is_data_centre = (building_type == BuildingTypeStatus.data_centre)
        is_hospital = (building_type == BuildingTypeStatus.hospital)
        is_hotel = (building_type == BuildingTypeStatus.hotel)
        is_office = (building_type == BuildingTypeStatus.office)
        is_shopping_centre = (building_type == BuildingTypeStatus.shopping_centre)
        return select([is_apartment_building, is_data_centre, is_hospital, is_hotel, is_office, is_shopping_centre],
            ['apartment_building', 'data_centre', 'hospital', 'hotel', 'office', 'shopping_centre'])


class postcode(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = "What is the postcode for the building you are calculating ESCs for?"
