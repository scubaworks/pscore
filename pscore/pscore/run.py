"""
- Search Yelp for the given term and location
- Pick the first result
- Get the risk of that business
- Compare with risk of nearby competition to get pscore
"""

import argparse
import logging
import sys
import os
import io
import json


from fetch_google_places import google_place_info
from fetch_yelp_places import yelp_nearby, yelp_find_place
from calc_pscore import calc_place_pscore

log = logging.getLogger('pscore')


def _get_place(term_str, location_str, bust_cache=False, limit=10):
    """
    Get place object from cache or reconstruct by calling APIs.
    """
    cache_dir = '/tmp/pscore_cache/'
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    path = '{}/{}__{}.json'.format(cache_dir, term_str.replace(' ', ''), location_str)
    if os.path.exists(path) and not bust_cache:
        with open(path, 'r') as f:
            place = json.load(f)
            place['nearby'] = place['nearby'][:limit]
    else:
        place = yelp_find_place(term_str, location_str)
        place.update(google_place_info(place))
        nearby_places = []
        for nearby in yelp_nearby(place, limit=limit):
            nearby.update(google_place_info(nearby))
            nearby_places.append(nearby)
        place['nearby'] = nearby_places

        with io.open(path, 'w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(place, ensure_ascii=False, indent=4)))

    log.info(u'Identified Business as "{}" with {} nearby competitors'.format(
        place['name'], len(place['nearby']))
    )
    return place


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('term_str', help='Yelp search string')
    parser.add_argument('location_str', help='Yelp location string')
    parser.add_argument('--limit', '-l', type=int, default=25, help='Nearby search')
    parser.add_argument('--bust-cache', action='store_true', help='Force new api calls')
    args = parser.parse_args()

    # Pipe log to stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    stdout_handler.setFormatter(formatter)
    log.addHandler(stdout_handler)
    log.setLevel(logging.INFO)
    stdout_handler.setLevel(logging.INFO)

    # Run
    place = _get_place(args.term_str, args.location_str, bust_cache=args.bust_cache, limit=args.limit)
    calc_place_pscore(place)

if __name__ == '__main__':
    main()
