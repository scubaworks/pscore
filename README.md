# P Score
The goal is to calculate a "P score" for a given small business using only publicly available APIs and data. The "P score" of a small business should be related to how likely it is to default on a 3­ year loan.

Most small businesses seeking loans are young and therefore hard to find public data on (e.g. Freebase). However a high percent of new businesses have a social media presence and market themselves on sites such as Yelp. 80% of small businesses are either restaurants or shops so they will likely be on Yelp anyways. In fact, lets assume that all small businesses are on Yelp.

For this example lets assume we want to investigate a loan application for Black Forest Brooklyn in Fort Greene (zip code 11217).

# Risk Factor
Studies show the most common reason restaurants and shops fail is:

- Failed Expectations: Failed to deliver the quality expected by their target market
- Real Estate: Could not keep up with rent increase

Risk Factor is the sum of Rent Risk and Expectations Risk, which are both explained below. (TODO factor in business age)


## Failed Expectations Risk
Expensive restaurants and shops typically focus on quality while cheaper places focus on quantity. Customer reviews are written based on whether these expectations were met. Good reviews are important for all businesses, but the impact of those reviews increases with price range. In a way this means 4 dollar signs and 1 star is the worst case, while 1 dollar sign and 5 stars is the best case. Checkout this table to see the possibilities (simplified with ratings and reviews from 1-3 only):

![expectations]((/screenshots/screen_a.png?raw=true))

The actual values we'll be using for price_level are (1) Inexpensive (2) Moderate (3) Expensive (4) Very Expensive. Yelp does not expose prices so we get this from Google Places. For rating we use an avg between 1.0 and 5.0 which comes from both Yelp and Google places. Note that one scale is from 1-4 and the other is from 1-5. To handle that offset we will always subtract 1 from the reviews, mostly because 1 star is terrible even for price_level 1. Expectation risk is calculated as follows:

```python
    expectation_offset = price_level - (avg_rating - 1)
    expectation_risk = expectation_offset * abs(expectation_offset)
```

The value of expectation_risk ranges from -9 (best) to 16 (worst).


## Rent Risk
Rent increases are a serious threat to small businesses. If their rent is increasing faster than their ability to meet or exceed expectations, then there is a good chance they'll default on the loan. Not only does higher rent increase the price of the operating space, but it also increases the cost of living for employees which will ultimately cost the business more money. Its unlikely that the business owner accounted for these increases when applying for the loan, which means they need to be performing even better than expected in order to pay it back on time.

To measure rent increase we access [Zillow data](http://www.zillow.com/research/data/) using Quandl. Specifically, we access the following by zip-code:

- Single Family Cost: Median estimated home value for all single-family homes
- Price to Rent Ratio: Ratio of home prices to annual rental rates

Given these numbers the monthly rent is calculated by ```(avg_single_family / prr) / 12```. As you can see the rent in Fort Green has increase 11 percent over the last 3 years, which is considerable (assume we are ignoring rent control)!

```
Date                       Single Family Cost         Monthly Rent
2013-12-31                 2231900                    7412
2014-12-31                 2609900                    8007
2015-12-31                 2881100                    8256
```


# pscore
These risk calculations alone are not very useful. But if we compare them with the risk values of nearby competitors it will give us a good idea of how likely they are to survive in the next 3 years given their surroundings. We can also better understand the past by targeting nearby competitors that have been around for over 3 years and see if this process would have predicted they'd still be around today.

Yelp is used to search for nearby competitors using category filters and a radius of 6000 from the applicants zip code. The entire process above (expectation risk, rent risk) is repeated for each competitor.

The next step is to quantify where the applicants risk lies in the range of its competitor's risks. This is TODO. Right now the pscore is risk value of the applicant and a list containing the risk values of nearby competitors. 


# More thoughts

## Other Considerations
- Looking more at age as a measure of credibility
- Using social media "checkins" as a measure of popularity
- Think more about the distance to use when comparing with nearby competitors. Rural areas should have a larger radius than suburban areas, which can be estimated by population density
- How to handle accuracy lost fewer ratings

## Summary of Assumptions
- All small businesses are on Yelp
- All small businesses on Yelp are also on Google Places
- All small businesses have exactly one location, which is rented
- All small businesses have been reviewed on Yelp and Google Places, and have a fair number of ratings relative to their competitors regardless of how old they are
- Online reviews accurately reflect quality, satisfaction, popularity, etc.
- All small businesses applying for loans already have customers
- Rent control does not exist


# Usage
```
$ virtualenv env
$ source env/bin/activate
$ python setup.py develop
$ python -m pscore.run 'black forest brooklyn' 'fort greene'
```
Example output:
![screenshot](/screenshots/screen_b.png?raw=true)

Note that I have API credentials in this public repo which is usually crazy but I will revoke them ASAP.

