import requests
import json

key =  'omv1Rp72n1GcXXHuWBCw'

#For the goodreads api:
def get_review_counts(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": isbn})
    json_data = res.json()

     # Get data we need (average_rating) from the JSON response
    average_rating = json_data['books'][0]['average_rating']
    number_ratings = json_data['books'][0]['work_ratings_count']
    if not average_rating:
        average_rating = "Not found"
    if not number_ratings:
        number_ratings = "Not found"

    # Store data in dict
    goodreads_result = {'average_rating': average_rating, 'number_ratings': number_ratings}

    return goodreads_result
