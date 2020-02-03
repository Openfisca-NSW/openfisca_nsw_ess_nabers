# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class current_NABERS_star_rating(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'The star rating associated with the current NABERS rating' \
            ' for which ESCs are registered and created, following review' \
            ' of the evidence of the created Energy Savings.' \
            ' need to find prescription date for this.'


class ESC_creation_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'The date on which ESCs are registered and created, following review' \
            ' of the evidence of the created Energy Savings.' \
            ' need to find prescription date for this.'


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
    label = "NABERS rating used to calculate ESCs must be current NABERS rating" \
        " In accordance to clause 8.8.2(a)." \


class star_rating_exceeds_method_one_benchmark_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = YEAR
    label = 'Checks whether the star rating input by the user exceeds the' \
            ' benchmark rating defined in Table A20 by at least 0.5 stars.' \
            ' In accordance with Clause 8.8.3 (a) (i).'

    def formula(buildings, period, parameters):
        current = buildings('current_NABERS_star_rating', period)
        benchmark = buildings('method_one', period)
        return where(current - benchmark >= 0.5, True, False)


class star_rating_exceeds_method_two_benchmark_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = YEAR
    label = 'Checks whether the star rating input by the user exceeds the' \
            ' Historical Benchmark NABERS Rating used in Calculation Method 2' \
            ' by at least 0.5 stars.' \
            ' In accordance with Clause 8.8.3 (b) (i).'

    def formula(buildings, period, parameters):
        current = buildings('current_NABERS_star_rating', period)
        benchmark = buildings('method_two', period)
        return where(current - benchmark >= 0.5, True, False)


class historical_baseline_no_more_than_7_years_before_current_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = YEAR
    label = "historical baseline must be calculated no more than 7 years before" \
        " the end date of the Current Rating Year" \
        " in accordance with clause 8.8.4 (a)"

    def formula(building, period, parameters):
        current = buildings(
            'end_date_of_current_nabers_rating_period', period)
        hist = buildings(
            'end_date_of_historical_nabers_rating_period', period
            )
        distance_between_current_and_historical_baseline = (
            current.astype('datetime64[D]') - hist.astype('datetime64[D]')).astype('datetime64[D]')
        distance_in_years = distance_between_current_and_historical_baseline.astype('datetime64[Y]')
        return distance_in_years <= 7


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
            ' Administrator which is listed in the NABERS Baseline Method Guide.' \
            ' In accordance with Clause 8.8.4 (c).'


class implementation_date(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = 'Implementation Date equals the end date of the Current Rating Period.' \
            ' The Implementation Date is the end date of the first Rating Period' \
            ' for which Energy Savings will be calculated under clause 8.8.7.' \
            ' In accordance with Clause 8.8.5.' \
            ' IPART NABERS method guide requires NABERS report to specify the' \
            ' end date of the rating period.'

    def formula(buildings, period, parameters):
        return buildings('end_date_of_current_nabers_rating_period', period)


class energy_saver(Variable):
    value_type = str
    entity = Building
    definition_period = YEAR
    label = 'Name of person on NABERS certificate, or building owner or manager' \
            ' of building owner or manager of buildings identified on NABERS' \
            ' Rating certificate if the person’s name is not identified on ' \
            ' the NABERS Rating certificate, as issued by the NABERS National' \
            ' Administrator, in respect of the NABERS Rating.' \
            ' In accordance with Clause 8.8.6.'


class energy_savings_date(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = 'Note identical to end date of Current NABERS Period.' \
            ' For the purposes of section 131 of the Act, Energy Savings are' \
            ' taken to occur on the date that the Scheme Administrator ' \
            ' determines that the relevant NABERS Rating was completed. ' \
            ' In accordance with Clause 8.8.7.'  # need to read guidance material.

    def formula(buildings, period, parameters):
        return buildings('end_date_of_current_nabers_rating_period', period)


class nabers_value_previously_used__to_set_historical_NABERS_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'NABERS Rating of the same value can only be used once to set'\
            ' a fixed Historical Baseline NABERS Rating for a NABERS Building.'\
            ' according to clause 8.8.10 (c).'


class nabers_value_lower_than_previous_historical_NABERS_value(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'A NABERS rating cannot be lower than a previous NABERS rating used' \
            ' to create a historical NABERS rating.'\
            ' according to clause 8.8.10 (c).'
