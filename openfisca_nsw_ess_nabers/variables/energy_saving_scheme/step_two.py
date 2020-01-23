# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *
import time
import numpy as np

epoch = time.gmtime(0).tm_year
t = time.time()
current_time = time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(t))


class method_one(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Benchmark NABERS Star Rating calculated using Calculation Method 1' \
            '(Step 2) of the NABERS Baseline Method (Method 4) in the ESS Rules'

    def formula(buildings, period, parameters):
        current_rating_year = buildings('current_rating_year', period)
        rating_year_string = where(current_rating_year > parameters(period).energy_saving_scheme.table_a20.max_year, parameters(period).energy_saving_scheme.table_a20.max_year, buildings('current_rating_year', period).astype('str'))
        building_type = buildings("building_type", period)
        built_before_or_after_nov_2006 = where(buildings('built_after_nov_2006', period), "built_after_nov_2006", "built_before_nov_2006")
        if (current_rating_year >= parameters(period).energy_saving_scheme.table_a20.min_year):
            year_count = parameters(period).energy_saving_scheme.table_a20.min_year - 1
            while (year_count < current_rating_year):
                year_count += 1
                return parameters(period).energy_saving_scheme.table_a20.ratings.by_year[rating_year_string][building_type][built_before_or_after_nov_2006]


class method_two(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Benchmark NABERS Star Rating calculated using Calculation Method 2' \
            ' (Step 2) of the NABERS Baseline Method (Method 4)'\
            ' As prescribed in Method 4 of the ESS Rule 2020.'  # need some help with this one referring to parameters

    def formula(buildings, period, parameters):
        hist_rating = buildings('historical_NABERS_star_rating', period)
        cur_year = buildings('current_rating_year', period)
        hist_year = buildings('historical_rating_year', period)
        rating_adjustment = parameters(period).energy_saving_scheme.table_a21


class first_nabers_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = "Is this the first NABERS rating for the NABERS Building?"


class rating_not_obt_for_legal_requirement(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = "Is the rating not being obtained in order to comply with any mandatory legal requirement imposed through a statutory or regulatory instrument of any jurisdiction, including, but not limited to, the Commercial Building Disclosure Program"


class method_one_can_be_used(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = "Can Method 1 be used to calculate the NABERS Benchmark Rating for the buildings?"

    def formula(buildings, period, parameters):
        return (buildings('first_nabers_rating', period) * (buildings('rating_not_obt_for_legal_requirement', period)))


class built_after_nov_2006(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = "Benchmark NABERS Rating calculated using Calculation Method 2 (Step 2) of the NABERS Baseline Method (Method 4) in the ESS Rules"


class start_date_of_current_nabers_rating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'The date on which the current rating period begins. The Rating' \
            ' Period is the time over which measurements were taken to' \
            ' establish the NABERS Rating or the Historical Baseline NABERS' \
            ' Rating for the NABERS Building' \
            ' As published within the NABERS Rating Report.'


class end_date_of_current_nabers_rating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = "The date on which the current rating period ends. The Rating Period is the time over which measurements were taken to establish the NABERS Rating or the Historical Baseline NABERS Rating for the NABERS Building"


class start_date_of_historical_nabers_rating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'The date on which the historical rating period begins. The Rating' \
            ' Period is the time over which measurements were taken to' \
            ' establish the NABERS Rating or the Historical Baseline NABERS' \
            ' Rating for the NABERS Building' \
            ' As published within the NABERS Rating Report.'


class end_date_of_historical_nabers_rating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'The date on which the historical rating period ends. The Rating' \
            ' Period is the time over which measurements were taken to' \
            ' establish the NABERS Rating or the Historical Baseline ' \
            ' NABERS Rating for the NABERS Building. '


class historical_NABERS_star_rating(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The star rating associated with the historical rating used to' \
            ' calculate Benchmark NABERS Rating within Calculation Method 2.'


class current_rating_period_length(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Calculates the length of the current rating period, based on the' \
            ' difference between the start date of the current rating period' \
            ' and the end date of the current rating period.' \
            ' the Rating Period is the time over which measurements were' \
            ' taken to establish the NABERS Rating or the Historical Baseline' \
            ' NABERS Rating for the NABERS Building; ' \
            ' In accordance with clause 8.8.2 (c).'

    def formula(buildings, period, parameters):
        end = buildings(
            'end_date_of_current_nabers_rating_period', period)
        start = buildings(
            'start_date_of_current_nabers_rating_period', period
            )
        return end.astype('datetime64[M]') - start.astype('datetime64[M]')


class historical_rating_period_length(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Calculates the length of the historical rating period, based on the' \
            ' difference between the start date of the current rating period' \
            ' and the end date of the historical rating period.' \
            ' the Rating Period is the time over which measurements were' \
            ' taken to establish the NABERS Rating or the Historical Baseline' \
            ' NABERS Rating for the NABERS Building; ' \
            ' In accordance with clause 8.8.2 (c).'

    def formula(buildings, period, parameters):
        end = buildings(
            'end_date_of_historical_nabers_rating_period', period)
        start = buildings(
            'start_date_of_historical_nabers_rating_period', period
            )
        return end.astype('datetime64[M]') - start.astype('datetime64[M]')


class historical_rating_age(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Calculates the age of a Historical NABERS rating, to determine' \
            ' which Annual Ratings Adjustment to use in Calculation Method 2'

    def formula(buildings, period, parameters):
        cur_time = time.time() + epoch
        hist_rating_date = buildings(
            'end_date_of_historical_nabers_rating_period', period
            )


class current_rating_year(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = "The year in which the Rating Period ends for the NABERS Rating"
    "and is the year for which Energy Savings Certificates will be created"

    def formula(buildings, period, parameters):
        end_date_of_current_nabers_rating_period = buildings('end_date_of_current_nabers_rating_period', period)
        current_rating_year = end_date_of_current_nabers_rating_period.astype('datetime64[Y]') + epoch  # need to check if this works on Windows
        return current_rating_year


class historical_rating_year(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'The year in which the Rating Period ends for the Historical NABERS' \
            ' Rating, used for defining the Historical NABERS Rating Period'

    def formula(buildings, period, parameters):
        end_date_of_historical_nabers_rating_period = buildings('end_date_of_historical_nabers_rating_period', period)
        historical_rating_year = end_date_of_historical_nabers_rating_period.astype('datetime64[Y]') + epoch
        return historical_rating_year


class time_between_historical_and_current_ratings_within_range(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Tests the distance between historical and current ratings against' \
            ' the maximum allowable distance, for forward creation within' \
            ' Method 2. In accordance with Clause 8.8.10 (b).'

    def formula(buildings, period, parameters):
        return (
            buildings('cur_his_diff_as_months', period) <=
            parameters(period).energy_saving_scheme.diff_historical_current_rating_forward_creation
            )


class cur_his_diff_as_months(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Calculates the difference in months between the historical NABERS' \
            ' rating period and the current NABERS rating period, for testing' \
            ' against time_between_historical_and_current_ratings_within_range.'

    def formula(buildings, period, parameters):
        cur = buildings(
            'end_date_of_current_nabers_rating_period', period)
        hist = buildings(
            'end_date_of_historical_nabers_rating_period', period
            )
        return cur.astype('datetime64[M]') - hist.astype('datetime64[M]')


class time_between_current_ratings_and_ESC_date_within_range(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Tests the distance between the end of the current rating period' \
            ' and the date of Energy Savings Certificates against the maximum' \
            ' allowable distance between end of rating and ESC creation date.' \
            ' In accordance with clause 8.8.8.'

    def formula(buildings, period, parameters):
        return (
            buildings('cur_ESC_diff_as_months', period) <=
            parameters(period).energy_saving_scheme.diff_current_rating_esc_creation_date
        )


class cur_ESC_diff_as_months(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Calculates the difference in months between the current NABERS' \
            ' period and the ESC creation date, for testing against' \
            ' time_between_current_ratings_and_ESC_date_within_range. '

    def formula(buildings, period, parameters):
        cur = buildings(
            'end_date_of_current_nabers_rating_period', period)
        ESC = buildings(
            'ESC_creation_date', period
            )
        return cur.astype('datetime64[M]') - ESC.astype('datetime64[M]')


class benchmark_nabers_rating(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Benchmark NABERS rating calculated using Method 1 or Method 2"

    def formula(buildings, period, parameters):
        return select([buildings('method_one_can_be_used', period)],
        [buildings('method_one', period)])
