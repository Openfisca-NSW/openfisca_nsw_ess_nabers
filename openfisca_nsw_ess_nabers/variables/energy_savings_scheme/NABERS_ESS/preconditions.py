# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *
from datetime import datetime


def find_corresponding_date(start_date):
    day = start_date.day
    month = start_date.month
    year = start_date.year
    next_month = month + 1
    next_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1

    try:
        new_date = datetime(year=next_year, month=next_month, day=day)
    except ValueError:
        next_month = next_month + 1
        if next_month == 13:
            next_month = 1
            next_year = next_year + 1
        new_date = datetime(year=next_year, month=next_month, day=1)
        return new_date

    else:
        return new_date


def count_months(start_date, end_date):
    count = 0
    corres_date = start_date
    while(True):
        corres_date = find_corresponding_date(corres_date)
        # print(corres_date)
        if(corres_date > end_date):
            return count
        else:
            count = count + 1


class current_NABERS_star_rating(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the current star rating for the NABERS rated building' \
            ' for which ESCs are being registered?'


class ESC_creation_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the date on which ESCs are registered and created?'\



class includes_GreenPower(Variable):
    value_type = bool
    entity = Building
    definition_period = YEAR
    label = "Does the NABERS rating include Greenpower?" \



class uses_NABERS_ratings_tool(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Was the NABERS rating calculated using one of the NABERS Rating' \
            ' Tools?'

    def formula(buildings, period, parameters):
        is_apartment_building = buildings('is_apartment_building', period)
        is_data_centre = buildings('is_data_centre', period)
        is_hospital = buildings('is_hospital', period)
        is_hotel = buildings('is_hotel', period)
        is_office = buildings('is_office', period)
        is_shopping_centre = buildings('is_shopping_centre', period)
        uses_NABERS_ratings_tool = (is_apartment_building + is_data_centre
        + is_hospital + is_hotel + is_office + is_shopping_centre)
        return uses_NABERS_ratings_tool


class meets_minimum_star_rating_requirement(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the star rating exceed the minimum star rating defined in' \
            ' Clause 8.8.3?'

    def formula(buildings, period, parameters):
        clause_8_8_3_a_i = buildings('star_rating_exceeds_method_one_benchmark_rating', period)
        clause_8_8_3_a_ii = buildings('first_nabers_rating', period)
        clause_8_8_3_a_iii = buildings('rating_not_obt_for_legal_requirement', period)
        clause_8_8_3_b = buildings('star_rating_exceeds_method_two_benchmark_rating', period)
        condition_method_one = (clause_8_8_3_a_i * clause_8_8_3_a_ii
        * clause_8_8_3_a_iii)
        condition_method_two = clause_8_8_3_b
        return condition_method_one + condition_method_two


class is_current_NABERS_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = YEAR
    label = 'Is the NABERS Rating used to calculate ESCs a current NABERS' \
            ' Rating?'


class star_rating_exceeds_method_one_benchmark_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the NABERS Star Rating used to calculate ESCs within' \
            ' method 1 exceed the minimum star rating?'

    def formula(buildings, period, parameters):
        current = buildings('current_NABERS_star_rating', period)
        benchmark = buildings('method_one', period)
        return where(current - benchmark >= 0.5, True, False)


class rating_not_obt_for_legal_requirement(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the rating not being obtained in order to comply with any' \
            ' mandatory legal requirement? This includes, but is not limited' \
            ' to the Commercial Building Disclosure Program.'


class first_nabers_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is this the first NABERS Rating for the building?'  # is there a way to match this against previous ratings, i.e.


class star_rating_exceeds_method_two_benchmark_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = YEAR
    label = 'Does the NABERS Star Rating used to calculate ESCs within' \
            ' method 1 exceed the minimum star rating?'

    def formula(buildings, period, parameters):
        current = buildings('current_NABERS_star_rating', period)
        benchmark = buildings('method_two', period)
        method_one_can_be_used = buildings('method_one_can_be_used', period)
        return where(method_one_can_be_used, False, current - benchmark >= 0.5)


class historical_baseline_no_more_than_7_years_before_current_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = YEAR
    label = "Is the Historical Baseline NABERS Rating calculated no more than" \
        " 7 years before the end date of the Current Rating Year?"

    def formula(buildings, period, parameters):
        cur = buildings(
            'current_rating_year', period)
        hist = buildings(
            'baseline_rating_year', period
            )
        condition_method_one_is_used = buildings('method_one_can_be_used', period)
        return where(condition_method_one_is_used, True,
        cur - hist <= 7)


class historical_baseline_more_than_7_years(Variable):
    value_type = bool
    entity = Building
    definition_period = YEAR
    label = "if Calculation Method 2 is to be used for Additional Energy Savings" \
        " and the fixed Historical Baseline NABERS Rating does not meet" \
        " requirements of 8.8.4 (a), it must be reset using using a previous" \
        " NABERS rating that is calculated at least 7 years later than" \
        " the end date of the previous fixed Historical baseline NABERS rating" \
        " in accordance with clause 8.8.4 (b)" \


    def formula(buildings, period, parameters):
        condition_method_one_is_used = buildings('method_one_can_be_used', period)
        # additional_energy_savings = buildings('additional_energy_savings_created', period)
        return where(condition_method_one_is_used, False,
        cur - hist <= 7)  # code in recalculation historical baseline based off previous historical rating - needs to be current_historical_rating - previous_historical_rating >= 7


class additional_energy_savings_created(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the NABERS Rating used to create ESCs for Additional Energy' \
            ' Savings?'  # probably need to code in the definition for this...


class historical_baseline_rating_meets_similar_configuration_criteria(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Historical Baseline NABERS Rating and the current NABERS' \
            ' Rating fulfill the similar configuration criteria?'


class implementation_date(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The Implementation Date means the end date of the Current Rating' \
            ' Period.'

    def formula(buildings, period, parameters):
        return buildings('end_date_of_current_nabers_rating_period', period)


class energy_saver(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'Who is the Energy Saver for the Implementation?'

    """
    def formula(buildings, period, parameters):
        NABERS_certificate_name = buildings('NABERS_certificate_name', period)
        building_owner_manager_name = buildings('building_owner_or_manager_name', period)
        condition_NABERS_cert_name

    """


class energy_savings_date(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = ' For the purposes of section 131 of the Act, Energy Savings are' \
            ' taken to occur on the date that the Scheme Administrator ' \
            ' determines that the relevant NABERS Rating was completed. ' \
            ' In accordance with Clause 8.8.7.'  # need to read guidance material.

    def formula(buildings, period, parameters):
        return buildings('NABERS_rating_completed_date', period)


class time_between_current_ratings_and_ESC_date_within_range(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Tests the distance between the end of the current rating period' \
            ' and the date of Energy Savings Certificates against the maximum' \
            ' allowable distance between end of rating and ESC creation date.' \
            ' In accordance with clause 8.8.8.'

    def formula(buildings, period, parameters):
        return (buildings('ESC_cur_diff_as_months', period)
        <= parameters(period).energy_savings_scheme.preconditions.distance_rating_end_ESCs)


class nabers_value_previously_used_to_set_historical_NABERS_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has a NABERS Rating of the same value previously been used to' \
            ' set a Historical Baseline NABERS Rating?'


class nabers_value_lower_than_previous_historical_NABERS_value(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the current or historical NABERS Star Rating lower than a' \
            ' previous Historical NABERS Star Rating?'


class previous_annual_creation_occurred(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has annual creation for this implementation already occurred?'


class NABERS_eligible_to_create_ESCs(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Determines whether the relevant NABERS rating(s) pass all of the' \
            ' precondition requirements defined in Clause 8.8.'

    def formula(buildings, period, parameters):
        clause_8_8_1_a = buildings('uses_NABERS_ratings_tool', period)
        clause_8_8_1_b = not_(buildings('includes_GreenPower', period))
        clause_8_8_1_c = buildings('meets_minimum_star_rating_requirement', period)
        clause_8_8_1_d = buildings('all_on_site_sources_identified', period)
        clause_8_8_1_e = buildings('unaccounted_elec_metered_and_recorded', period)
        clause_8_8_1 = (clause_8_8_1_a * clause_8_8_1_b * clause_8_8_1_c
        * clause_8_8_1_d * clause_8_8_1_e)
        clause_8_8_3_a_i = buildings('star_rating_exceeds_method_one_benchmark_rating', period)
        clause_8_8_3_a_ii = buildings('first_nabers_rating', period)
        clause_8_8_3_a_iii = buildings('rating_not_obt_for_legal_requirement', period)
        clause_8_8_3_b = buildings('star_rating_exceeds_method_two_benchmark_rating', period)
        clause_8_8_3 = (clause_8_8_3_a_i * clause_8_8_3_a_ii * clause_8_8_3_a_iii
        + clause_8_8_3_b)
        clause_8_8_4_a = buildings('historical_baseline_no_more_than_7_years_before_current_rating', period)
        clause_8_8_4_c = buildings('historical_baseline_rating_meets_similar_configuration_criteria', period)
        clause_8_8_4 = (clause_8_8_4_a
        * clause_8_8_4_c)
        clause_8_8_8 = buildings('time_between_current_ratings_and_ESC_date_within_range', period)
        clause_8_8_10_b = buildings('time_between_historical_and_current_ratings_within_range', period)
        clause_8_8_10_c_i = not_(buildings('nabers_value_previously_used_to_set_historical_NABERS_rating', period))
        clause_8_8_10_c_ii = not_(buildings('nabers_value_lower_than_previous_historical_NABERS_value', period))
        clause_8_8_10 = clause_8_8_10_b * clause_8_8_10_c_i * clause_8_8_10_c_ii
        return clause_8_8_1 * clause_8_8_3 * clause_8_8_4 * clause_8_8_8 * clause_8_8_10
