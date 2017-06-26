from googleplaces import GooglePlaces
import logging


_client = None
log = logging.getLogger('pscore')


def _get_client():
    global _client
    if _client:
        return _client
    key = 'AIzaSyDlgOkw-eGS3sf9C1Ov0FnBezAH8eJcxj4'
    _client = GooglePlaces(key)
    return _client


def google_place_info(place):
    log.info(u'Searching Google Places for {}'.format(place['name']))
    client = _get_client()
    resp = client.text_search(
        query=place['name'],
        lat_lng={'lat': place['lat'], 'lng': place['lng']},
        radius=500,  # should be ver close!
    )
    assert len(resp.places), 'Could not find place'
    details = resp.places[0]
    details.get_details()
    keys = ('user_ratings_total', 'rating', 'price_level')
    return {'google_%s' % k: int(details.details[k]) for k in keys}
