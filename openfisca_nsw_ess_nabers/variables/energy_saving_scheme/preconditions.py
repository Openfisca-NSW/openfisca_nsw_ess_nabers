# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class includes_GreenPower(Variable):
    value_type = bool
    entity = Building
    definition_period = YEAR
    label = "whether the NABERS rating includes Greenpower" \
        " NABERS rating must exclude GreenPower" \
        " in accordance to clause 5.4" \
        " “GreenPower” means renewable energy purchased" \
        " in accordance with the National GreenPower" \
        " Accreditation Program Rules. "


class is_current_NABERS_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = YEAR
    label = "NABERS rating must be current NABERS rating" \
        " in accordance to clause 8.8.2(a)" \
        " energy savings must be calculated from current rating"


class historical_baseline_no_more_than_7_years_before_current_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = YEAR
    label = "historical baseline must be calculated no more than 7 years before" \
        " the end date of the Current Rating Year" \
        " in accordance with clause 8.8.4 (a)"

    def formula(building, period, parameters):
        return (current_rating_year - historical_rating_year) <= 7


class calculation_used_for_additional_savings(Variable):
    value_type = bool
    entity = Building
    definition_period = YEAR
    label = "if Calculation Method 2 is to be used for Additional Energy Savings" \
        " and the fixed Historical Baseline NABERS Rating does not meet" \
        " requirements of 8.8.4 (a), it must be reset using using a previous" \
        " NABERS rating that is calculated at least 7 years later than" \
        " the end date of the previous fixed Historical baseline NABERS rating" \
        " in accordance with clause 8.8.4 (b)" \


class historical_baseline_rating_meets_similar_configuration_criteria(Variable):
    value_type = bool
    entity = Building
    definition_period = YEAR
    label = "the Historical Baseline NABERS Rating must meet the ‘similar" \
            " configuration criteria that has been determined by the Scheme " \
            " Administrator which is listed in the NABERS Baseline Method Guide. "


class maximum_years_of_forward_creation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "maximum allowable time to forward create for, maximum 3 years" \
            " the maximum time period for "

    def formula(buildings, period, parameters):
        condition_forward_creation = building('years_of_forward_creation', period) > 3
        return where(condition_forward_creation, 3 + "maximum number of years for forward creation is 3", 'years_of_forward_creation')


class nabers_value_previously_used__to_set_historical_NABERS_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'NABERS Rating of the same value can only be used once to set'\
            ' a fixed Historical Baseline NABERS Rating for a NABERS Building.'\
            ' according to clause 8.8.10 (c).'
