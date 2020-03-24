# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *
import time
import numpy as np
import datetime
from datetime import datetime as py_datetime
from numpy import datetime64 as np_datetime
import pandas as pd

epoch = time.gmtime(0).tm_year
today_date_and_time = np.datetime64(datetime.datetime.now())
today = today_date_and_time.astype('datetime64[D]')


def find_corresponding_date(start_date):
    day = start_date.day
    month = start_date.month
    year = start_date.year
    next_month = month + 1
    next_year = year

    if month == 12:
        next_month = 1
        next_year = year+1
    try:
        new_date = np_datetime(year=next_year, month=next_month, day=day)
    except ValueError:
        next_month = next_month + 1
        if next_month == 13:
            next_month = 1
            next_year = next_year+1
        new_date = np_datetime(year=next_year, month=next_month, day=1)
        return new_date

    else:
        return new_date


def count_months(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    count = 0
    corres_date = start_date
    while(True):
        corres_date = find_corresponding_date(corres_date)
        if(corres_date > end_date):
            return count
            break
        else:
            count = count + 1



class method_one(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Benchmark NABERS Star Rating calculated using Calculation Method 1' \
            '(Step 2) of the NABERS Baseline Method (Method 4) in the ESS Rules'

    def formula(buildings, period, parameters):
        current_rating_year = buildings('current_rating_year', period)
        rating_year_string = where(current_rating_year
        > parameters(period).energy_savings_scheme.table_a20.max_year,
        parameters(period).energy_savings_scheme.table_a20.max_year,
        buildings('current_rating_year', period).astype('str'))
        building_type = buildings("building_type", period)
        built_before_or_after_nov_2006 = where(buildings('built_after_nov_2006', period),
        "built_after_nov_2006",
        "built_before_nov_2006")
        if (current_rating_year >= parameters(period).energy_savings_scheme.table_a20.min_year):
            year_count = parameters(period).energy_savings_scheme.table_a20.min_year - 1
            while (year_count < current_rating_year):
                year_count += 1
                return (parameters(period).energy_savings_scheme.table_a20.ratings.by_year
                [rating_year_string][building_type][built_before_or_after_nov_2006])


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
        hist_year = buildings('baseline_rating_year', period)
        building_type = buildings("building_type", period)
        hist_rating_age = buildings('age_of_historical_rating', period)
        adjustment_year_string = where(hist_rating_age > 1,
        "two_to_seven_year_old",
        "one_year_old")
        annual_rating_adj = (parameters(period).energy_savings_scheme.table_a21.building_category
        [building_type][adjustment_year_string])
        return hist_rating + annual_rating_adj * (cur_year - hist_year)


class rating_not_obt_for_legal_requirement(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the rating not being obtained in order to comply with any' \
            ' mandatory legal requirement imposed through a statutory or ' \
            ' regulatory instrument of any jurisdiction, including, but not' \
            ' limited to, the Commercial Building Disclosure Program.' \
            ' In accordance with clause 8.8.3 (a) (iii).'


class method_one_can_be_used(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = "Can Method 1 be used to calculate the NABERS Benchmark Rating for the buildings?"

    def formula(buildings, period, parameters):
        return (buildings('first_nabers_rating', period)
        * (buildings('rating_not_obt_for_legal_requirement', period)))


class built_after_nov_2006(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Determines whether the building was built after November 2006,' \
            ' in order to determine the appropriate benchmark rating to use' \
            ' within Calculation Method 1 of the NABERS method.'


class start_date_of_current_nabers_rating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'The date on which the current rating period begins. The Rating' \
            ' Period is the time over which measurements were taken to' \
            ' establish the NABERS Rating or the Historical Baseline NABERS' \
            ' Rating for the NABERS Building' \
            ' As published within the NABERS Rating Report.' \
            ' As defined in Clause 8.8.2 (a).'


class end_date_of_current_nabers_rating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'The date on which the current rating period ends. The Rating' \
            ' Period is the time over which measurements were taken to' \
            ' establish the NABERS Rating or the Historical Baseline NABERS' \
            ' Rating for the NABERS Building.' \
            ' As published within the NABERS Report.' \
            ' As defined in Clause 8.8.2 (a).'


class start_date_of_historical_nabers_rating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'The date on which the historical rating period begins. The Rating' \
            ' Period is the time over which measurements were taken to' \
            ' establish the NABERS Rating or the Historical Baseline NABERS' \
            ' Rating for the NABERS Building' \
            ' As published within the NABERS Rating Report.' \
            ' As defined in Clause 8.8.2 (b).'


class end_date_of_historical_nabers_rating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'The date on which the historical rating period ends. The Rating' \
            ' Period is the time over which measurements were taken to' \
            ' establish the NABERS Rating or the Historical Baseline ' \
            ' NABERS Rating for the NABERS Building.' \
            ' As defined in Clause 8.8.2 (b).'


class historical_NABERS_star_rating(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The star rating associated with the historical rating used to' \
            ' calculate Benchmark NABERS Rating within Calculation Method 2.' \
            ' As defined in clause 8.8.2 (b)'


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
        end_date = (buildings(
            'end_date_of_current_nabers_rating_period', period
            ).astype('datetime64[D]'))
        start_date = (buildings(
            'start_date_of_current_nabers_rating_period', period
            ).astype('datetime64[D]'))
        import pdb; pdb.set_trace()
        rating_period_length = count_months(start_date, end_date)
        return rating_period_length # need to redefine months as defined in Interpretations Act - as period from period between defined day and the corresponding day in the following month


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
        end = buildings('end_date_of_historical_nabers_rating_period', period)
        start = buildings('start_date_of_historical_nabers_rating_period', period)
        return end.astype('datetime64[M]') - start.astype('datetime64[M]')


class current_rating_year(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'The year in which the Rating Period ends for the NABERS Rating' \
    'and is the year for which Energy Savings Certificates will be created' \
    ' As defined in Clause 8.8.2 (d).'

    def formula(buildings, period, parameters):
        end_date_of_current_nabers_rating_period = buildings('end_date_of_current_nabers_rating_period', period)
        current_rating_year = end_date_of_current_nabers_rating_period.astype('datetime64[Y]') + epoch  # need to check if this works on Windows
        return current_rating_year


class baseline_rating_year(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'The year in which the Rating Period ends for the Historical NABERS' \
            ' Rating, used for defining the Historical NABERS Rating Period' \
            ' As defined in Clause 8.8.2 (e).'

    def formula(buildings, period, parameters):
        end_date_of_historical_nabers_rating_period = buildings('end_date_of_historical_nabers_rating_period', period)
        baseline_rating_year = end_date_of_historical_nabers_rating_period.astype('datetime64[Y]') + epoch
        return baseline_rating_year


class time_between_historical_and_current_ratings_within_range(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Tests the distance between historical and current ratings against' \
            ' the maximum allowable distance, for forward creation within' \
            ' Method 2. In accordance with Clause 8.8.10 (b).'

    def formula(buildings, period, parameters):
        current_rating_day = buildings('end_date_of_current_nabers_rating_period', period).astype('datetime64[D]')
        historical_rating_day = buildings('end_date_of_historical_nabers_rating_period', period).astype('datetime64[D]')
        condition_method_one_is_used = buildings('method_one_can_be_used', period)
        condition_is_past_corresponding_day_in_following_month = current_rating_day >= historical_rating_day
        return select(
            [condition_method_one_is_used == True,
            condition_method_one_is_used == False and
            condition_is_past_corresponding_day_in_following_month == True,
            condition_method_one_is_used == False and
            condition_is_past_corresponding_day_in_following_month == False], [1,
            buildings('cur_his_diff_as_months', period) <=
            parameters(period).energy_savings_scheme.preconditions.historical_benchmark_age,
            (buildings('cur_his_diff_as_months', period)) - 1 <=
            parameters(period).energy_savings_scheme.preconditions.historical_benchmark_age])


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


class ESC_cur_diff_as_months(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Calculates the difference in months between the ESC creation date' \
            ' the current NABERS rating period, for testing' \
            ' against time_between_historical_and_current_ratings_within_range.'

    def formula(buildings, period, parameters):
        cur = buildings(
            'end_date_of_current_nabers_rating_period', period)
        ESC = buildings(
            'ESC_creation_date', period
            )
        return ESC.astype('datetime64[M]') - cur.astype('datetime64[M]')


class today_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'today date'

    def formula(buildings, period, parameters):
        return today


class age_of_historical_rating(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Calculate the age of the historical rating, for use in determining' \
            ' Annual Rating Adjustment from Table A21.' # need to determine what unit is used to determine the age of the historical rating.

    def formula(buildings, period, parameters):
        today = buildings(
            'today_date', period)
        hist = buildings(
            'end_date_of_historical_nabers_rating_period', period
            )
        age_in_days = (today.astype('datetime64[D]')
        - hist.astype('datetime64[D]')).astype('datetime64[D]')
        return age_in_days.astype('datetime64[Y]')


class benchmark_nabers_rating(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Benchmark NABERS rating calculated using Method 1 or Method 2"

    def formula(buildings, period, parameters):
        method_one = buildings('method_one', period)
        method_two = buildings('method_two', period)
        condition_method_one = buildings('method_one_can_be_used', period) == True
        return where (condition_method_one, method_one, method_two)
