from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator


_client = None


def _get_client():
    global _client
    if _client:
        return _client
    auth = Oauth1Authenticator(
        consumer_key='r2FPg3DG1R78UVr0gaxFAQ',
        consumer_secret='5dd8d9T_NN_rjZZV96D1RK-T_cU',
        token='ubu4RpZLbAjpMgMBITb8ACnoWQfaRDgH',
        token_secret='cg37u0D4O2HtM93myp0BI8_PRYg'
    )
    _client = Client(auth)
    return _client


def _format_place(p):
    return {
        'yelp_id': p.id,
        'rating': p.rating,
        'review_count': p.review_count,
        'zip_code': p.location.postal_code,
        'lat': p.location.coordinate.latitude,
        'lng': p.location.coordinate.longitude,
        'categories': [c.alias for c in p.categories],
        'name': p.name
    }


def yelp_find_place(term_str, location_str):
    found_places = yelp_search(term_str, location_str, limit=1)
    assert len(found_places), 'Yelp did not return any results for that query'
    return found_places[0]


def yelp_search(term, location, limit=1):
    client = _get_client()
    resp = client.search(location, term=term, lang='en', limit=limit)
    return [_format_place(r) for r in resp.businesses]


def yelp_nearby(place, limit=10):
    client = _get_client()
    location = place['zip_code']
    params = {
        'lang': 'en',
        'limit': limit,
        'category_filter': ','.join(place['categories']),
        'sort': 1,  # 0=Best matched (default), 1=Distance, 2=Highest Rated
        'radius_filter': 6000,  # in meters
    }
    resp = client.search(location, **params)
    return [_format_place(r) for r in resp.businesses]
