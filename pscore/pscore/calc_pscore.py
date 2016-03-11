
import logging
import numpy

from fetch_rent import fetch_rent_increase

log = logging.getLogger('pscore')


def calc_expectation_risk(price_level, avg_rating):
    """
        price_level:
            1 - Inexpensive
            2 - Moderate
            3 - Expensive
            4 - Very Expensive

    Note that one scale is from 1-4 and the other is from 1-5.
    To handle that offset we will always subtract 1 from the reviews,
    mostly because 1 star is terrible even for price_level 1 
    """
    expectation_offset = price_level - (avg_rating - 1)
    expectation_risk = expectation_offset * abs(expectation_offset)
    return expectation_risk


def calc_rent_risk(zip_code):
    rent_increase = fetch_rent_increase(zip_code)
    return rent_increase * 10


def calc_place_risk(place):
    """Calculate risk for a single place"""
    avg_rating = numpy.average([place['rating'], place['google_rating']])
    expectation_risk = calc_expectation_risk(place['google_price_level'], avg_rating)
    rent_risk = calc_rent_risk(place['zip_code'])
    total_risk = expectation_risk + rent_risk
    log.info(u'{:>30}   {:>5}   {:>6}   {:>6}   {:>6}   {:>6}'.format(
        place['name'][:28],
        place['google_price_level'],
        '{:.1f}'.format(avg_rating),
        '{:.3f}'.format(expectation_risk),
        '{:.3f}'.format(rent_risk),
        '{:.3f}'.format(total_risk))
    )
    return total_risk


def calc_place_pscore(place):
    """Compare risk with risk of nearby competition to get pscore."""
    log.info('{:>30}   Price   Rating   E_RISK   R_RISK     RISK'.format('Business'))

    place_risk = calc_place_risk(place)
    nearby_risks = [calc_place_risk(p) for p in place['nearby']]

    log.info('Standard Deviation: {}'.format(numpy.std(numpy.array([nearby_risks]))))
    log.info('Variance Deviation: {}'.format(numpy.var(numpy.array([nearby_risks]))))

    avg_risk = numpy.average(nearby_risks)
    median_risk = numpy.median(nearby_risks)
    log.info('Average Risk: {}'.format(avg_risk))
    log.info('Median Risk: {}'.format(median_risk))
    log.info('Versus "{}" Risk: {}'.format(place['name'], place_risk))
