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
from numpy import timedelta64


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
        new_date = py_datetime(year=next_year, month=next_month, day=day)
    except ValueError:
        next_month = next_month + 1
        if next_month == 13:
            next_month = 1
            next_year = next_year+1
        new_date = py_datetime(year=next_year, month=next_month, day=1)
        return new_date

    else:
        return new_date



def toPyDateTime(numpyDate):
    return py_datetime.strptime(str(numpyDate), "%Y-%m-%d")


def count_months(sdate, edate):
    start_date = toPyDateTime(sdate)
    end_date = toPyDateTime(edate)
    count = 0
    corres_date = start_date
    while(True):
        corres_date = find_corresponding_date(corres_date)
        if(corres_date > end_date):
            return count
            break
        else:
            count = count + 1

# above is the find_corresponding_date and count_months functions.
# this is code used to make the definition of "calendar month" as defined
# in the NSW Interpretations Act (1987) function as legally defined by DPIE
# Legal.

class method_one(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Benchmark NABERS Rating calculated using Method 1' \
            ' of the NABERS Baseline Method in the ESS?'

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
        if ((current_rating_year >= parameters(period).energy_savings_scheme.table_a20.min_year).any()):
            year_count = parameters(period).energy_savings_scheme.table_a20.min_year - 1
            while ((year_count < current_rating_year).any()):
                year_count += 1
                return (parameters(period).energy_savings_scheme.table_a20.ratings.by_year
                [rating_year_string][building_type][built_before_or_after_nov_2006])
        # the last line searches Table A20 using the user inputs for 1.
        # rating year, 2. building_type, 3. the boolean value of "built after
        # November 2006".


class method_two(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Benchmark NABERS Rating calculated using Method 1' \
            ' of the NABERS Baseline Method in the ESS?'

    def formula(buildings, period, parameters):
        hist_rating = buildings('historical_NABERS_star_rating', period)
        prev_hist_rating = buildings('previous_historical_baseline_rating', period)
        cur_year = buildings('current_rating_year', period)
        hist_year = buildings('baseline_rating_year', period)
        building_type = buildings("building_type", period)
        hist_rating_age = buildings('age_of_historical_rating', period)
        adjustment_year_string = where(hist_rating_age > 1,
        "two_to_seven_year_old",
        "one_year_old")
        annual_rating_adj = (parameters(period).energy_savings_scheme.table_a21.building_category
        [building_type][adjustment_year_string])
        condition_previous_forward_creation = buildings('previous_forward_creation_occurred', period)
        return where (condition_previous_forward_creation
        , prev_hist_rating + annual_rating_adj * (cur_year - hist_year)
        , hist_rating + annual_rating_adj * (cur_year - hist_year))
        # Condition forward previous annual creation is used to pull the fixed
        # historical baseline rating, as required by clause 8.8.11 (b).


class previous_forward_creation_occurred(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has previous forward creation occurred for this implementation' \
            ' within the previous 6 years?'


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
    label = 'Was the building built on or after 1 November 2006?'


class start_date_of_current_nabers_rating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the start date of the Current Rating Period as listed on' \
            ' the Current NABERS Rating Report?'


class end_date_of_current_nabers_rating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the end date of the Current Rating Period as listed on' \
            ' the Current NABERS Rating Report?'


class start_date_of_historical_nabers_rating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the start date of the Historical Rating Period as listed on' \
            ' the Historical NABERS Rating Report?' # probably need to put in a default value maybe?


class end_date_of_historical_nabers_rating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the end date of the Historical Rating Period as listed on' \
            ' the Historical NABERS Rating Report?'


class historical_NABERS_star_rating(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Star Rating of the Historical NABERS Rating, as listed' \
            ' on the Historical NABERS Rating Report?'

class current_rating_period_length(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the length of the Current NABERS Rating Period, as' \
            ' using the current start date and current end date?'

    def formula(buildings, period, parameters):
        end_date = (buildings(
            'end_date_of_current_nabers_rating_period', period
            ).astype('datetime64[D]'))
        start_date = (buildings(
            'start_date_of_current_nabers_rating_period', period
            ).astype('datetime64[D]'))
        rating_period_length = np.fromiter(map(count_months, start_date, end_date),int)
        return rating_period_length
        # fromiter pulls the count_months function, maps the start date and
        # end date to the function, and then returns the result as an array.
        # this is required due to OpenFISCA returning results as arrays.


class historical_rating_period_length(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the length of the Historical NABERS Rating Period, as' \
            ' using the historical start date and historical end date?'

    def formula(buildings, period, parameters):
        end_date = (buildings(
            'end_date_of_historical_nabers_rating_period', period
            ).astype('datetime64[D]'))
        start_date = (buildings(
            'start_date_of_historical_nabers_rating_period', period
            ).astype('datetime64[D]'))
        rating_period_length = np.fromiter(map(count_months, start_date, end_date),int)
        return rating_period_length
        # fromiter pulls the count_months function, maps the start date and
        # end date to the function, and then returns the result as an array.
        # this is required due to OpenFISCA returning results as arrays.

class current_rating_year(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the year for the current rating period?'

    def formula(buildings, period, parameters):
        end_date_of_current_nabers_rating_period = buildings('end_date_of_current_nabers_rating_period', period)
        current_rating_year = end_date_of_current_nabers_rating_period.astype('datetime64[Y]') + epoch  # need to check if this works on Windows
        return current_rating_year
        # + epoch is required to ensure that getting the current_rating_year
        # is consistent across platforms.

class end_date_of_current_rating_year(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = "What is the end date of the current rating year?"

    def formula(buildings, period, parameters):
        current_rating_year = buildings('current_rating_year', period).astype('datetime64[Y]')
        next_year = current_rating_year + np.timedelta64(1, 'Y')
        end_date_of_current_rating_year = next_year - np.timedelta64(1, 'D')
        return end_date_of_current_rating_year


class baseline_rating_year(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the year for the historical rating period?'

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
        end_date = buildings('end_date_of_current_nabers_rating_period', period).astype('datetime64[D]')
        start_date = buildings('end_date_of_historical_nabers_rating_period', period).astype('datetime64[D]')
        condition_method_one_is_used = buildings('method_one_can_be_used', period)
        current_historical_date_distance = np.fromiter(map(count_months, start_date, end_date),int)
        return select(
            [condition_method_one_is_used == True,
            condition_method_one_is_used == False], [1,
            buildings('current_historical_date_distance', period) <=
            parameters(period).energy_savings_scheme.preconditions.historical_benchmark_age])
            # fromiter pulls the count_months function, maps the start date and
            # end date to the function, and then returns the result as an array.
            # this is required due to OpenFISCA returning results as arrays.


class current_historical_date_distance(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Calculates the difference in months between the historical NABERS' \
            ' rating period and the current NABERS rating period, for testing' \
            ' against time_between_historical_and_current_ratings_within_range.'

    def formula(buildings, period, parameters):
        end_date = buildings(
            'end_date_of_current_nabers_rating_period', period)
        start_date = buildings(
            'end_date_of_historical_nabers_rating_period', period
            )
        distance_between_ratings = np.fromiter(map(count_months, start_date, end_date),int)
        return distance_between_ratings
        # fromiter pulls the count_months function, maps the start date and
        # end date to the function, and then returns the result as an array.
        # this is required due to OpenFISCA returning results as arrays.


class ESC_cur_diff_as_months(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Calculates the difference in months between the ESC creation date' \
            ' the current NABERS rating period, for testing' \
            ' against time_between_historical_and_current_ratings_within_range.'

    def formula(buildings, period, parameters):
        start_date = buildings(
            'end_date_of_current_nabers_rating_period', period)
        end_date = buildings(
            'ESC_creation_date', period
            )
        distance_between_rating_and_creation = np.fromiter(map(count_months,
        start_date, end_date),int)
        return distance_between_rating_and_creation
        # fromiter pulls the count_months function, maps the start date and
        # end date to the function, and then returns the result as an array.
        # this is required due to OpenFISCA returning results as arrays.


class today_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the date for today?'

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
        # returns difference between the the historical rating date and today
        # as a datetime64 year object. You need to review the test cases
        # associated with this with Andrew. This is not working as intended.
        # Need to find a definition of 'year' (likely start of day to
        # immediately before the corresponding day in the following year.)


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

class previous_historical_baseline_rating(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY  # need to check whether these inputs, on the NABERS reports, should all be year
    label = 'If there has been a previous Historical NABERS Baseline Rating' \
            ' what is the previous Historical NABERS Baseline Rating?'
            # Ilona my understanding is this is a Historical Baseline Rating"
            # and not a Benchmark Rating and as such will always be in 0.5
            # increments (unless NABERS introduces in between 0.5 ratings).
            # Please confirm.
