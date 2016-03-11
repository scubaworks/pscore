from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

import Quandl

log = logging.getLogger('pscore')


def fetch_rent_increase(zip_code):
    """
        A: All Homes
        SF: Single Family Residences
        PRR: Price-to-Rent Ratio

    https://www.quandl.com/blog/api-for-housing-data
    http://www.zillow.com/research/data/
    """
    three_years_ago = (datetime.now() - relativedelta(years=3)).strftime('%Y-%m-%d')
    set_names = ['ZILL/Z{}_{}'.format(zip_code, prefix) for prefix in ('SF', 'PRR')]
    sets = Quandl.get(set_names, trim_start=three_years_ago,
        collapse='annual', authtoken='aYWzBvA5SqPkY44GmB5g')
    rent_values = []
    for timestamp, series in sets.iterrows():
        try:
            avg_single_family = series['ZILL.Z{}_SF - Value'.format(zip_code)]
            prr = series['ZILL.Z{}_PRR - Value'.format(zip_code)]
        except KeyError:
            continue
        monthly_rent = (avg_single_family / float(prr)) / float(12)
        rent_values.append(monthly_rent)
    if not rent_values:
        return 0
    increased_by = (rent_values[-1] - rent_values[0]) / rent_values[-1]
    return increased_by
