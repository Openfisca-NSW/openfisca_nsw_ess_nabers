# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *
from datetime import datetime


class current_NABERS_star_rating(Variable):
    value_type = float
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


class uses_NABERS_ratings_tool(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Determines whether the NABERS Rating was calculated using one' \
            ' of the NABERS Rating Tools, as prescribed in Clause 8.8.1 (a).'

    def formula(buildings, period, parameters):
        is_apartment_building = buildings('is_apartment_building', period)
        is_data_centre = buildings('is_data_centre', period)
        is_hospital = buildings('is_hospital', period)
        is_hotel = buildings('is_hotel', period)
        is_office = buildings('is_office', period)
        is_shopping_centre = buildings('is_shopping_centre', period)
        uses_NABERS_ratings_tool = is_apartment_building + is_data_centre + is_hospital + is_hotel + is_office + is_shopping_centre
        return uses_NABERS_ratings_tool


class meets_minimum_star_rating_requirement(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Checks whether the Current NABERS Rating meets the eligibility' \
            ' criteria as prescribed in Clause 8.8.1(c).'

    def formula(buildings, period, parameters):
        clause_8_8_3_a_i = buildings('star_rating_exceeds_method_one_benchmark_rating', period)
        clause_8_8_3_a_ii = buildings('first_nabers_rating', period)
        clause_8_8_3_a_iii = buildings('rating_not_obt_for_legal_requirement', period)
        clause_8_8_3_b = buildings('star_rating_exceeds_method_two_benchmark_rating', period)
        condition_method_one = clause_8_8_3_a_i * clause_8_8_3_a_ii * clause_8_8_3_a_iii
        condition_method_two = clause_8_8_3_b
        return condition_method_one + condition_method_two


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


class first_nabers_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = "Tests whether the NABERS rating used in Calculation Method 1" \
        ' is the first NABERS Rating for the building.' \
        ' in accordance with clause 8.8.3 (a) (ii).' # is there a way to match this against previous ratings, i.e.


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

    def formula(buildings, period, parameters):
        cur = buildings(
            'current_rating_year', period)
        hist = buildings(
            'baseline_rating_year', period
            )
        condition_method_one_is_used = buildings('method_one_can_be_used', period)
        return where (condition_method_one_is_used, True,
        cur - hist <= 7)


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
            ' In accordance with Clause 8.8.4 (c).' # Note to Andrew - should we include IPART's similar configuration criteria? It is not strictly part of the rule.


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


class time_between_current_ratings_and_ESC_date_within_range(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Tests the distance between the end of the current rating period' \
            ' and the date of Energy Savings Certificates against the maximum' \
            ' allowable distance between end of rating and ESC creation date.' \
            ' In accordance with clause 8.8.8.'

    def formula(buildings, period, parameters):
        return buildings('ESC_cur_diff_as_months', period) <= parameters(period).energy_savings_scheme.preconditions.distance_rating_end_ESCs


class nabers_value_previously_used_to_set_historical_NABERS_rating(Variable):
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
        clause_8_8_1 = (clause_8_8_1_a * clause_8_8_1_b * clause_8_8_1_c *
        clause_8_8_1_d * clause_8_8_1_e)
        clause_8_8_3_a_i = buildings('star_rating_exceeds_method_one_benchmark_rating', period)
        clause_8_8_3_a_ii = buildings('first_nabers_rating', period)
        clause_8_8_3_a_iii = buildings('rating_not_obt_for_legal_requirement', period)
        clause_8_8_3_b = buildings('star_rating_exceeds_method_two_benchmark_rating', period)
        clause_8_8_3 = (clause_8_8_3_a_i * clause_8_8_3_a_ii * clause_8_8_3_a_iii +
        clause_8_8_3_b)
        clause_8_8_4_a = buildings('historical_baseline_no_more_than_7_years_before_current_rating', period)
        clause_8_8_4_c = buildings('historical_baseline_rating_meets_similar_configuration_criteria', period)
        clause_8_8_4 = (clause_8_8_4_a * clause_8_8_4_c)
        clause_8_8_8 = buildings('time_between_current_ratings_and_ESC_date_within_range', period)
        clause_8_8_10_b = buildings('time_between_historical_and_current_ratings_within_range', period)
        clause_8_8_10_c_i = not_(buildings('nabers_value_previously_used_to_set_historical_NABERS_rating', period))
        clause_8_8_10_c_ii = not_(buildings('nabers_value_lower_than_previous_historical_NABERS_value', period))
        clause_8_8_10 = clause_8_8_10_b * clause_8_8_10_c_i * clause_8_8_10_c_ii
        return clause_8_8_1 * clause_8_8_3 * clause_8_8_4 * clause_8_8_8 * clause_8_8_10
