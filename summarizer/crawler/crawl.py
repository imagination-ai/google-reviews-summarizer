import googlemaps
import os
from dataclasses import dataclass
import json

GOOGLE_REVIEWS_API_KEY = os.environ["GOOGLE_REVIEWS_API_KEY"]
GOOGLE_REVIEWS_CLIENT = googlemaps.Client(key=GOOGLE_REVIEWS_API_KEY)


@dataclass
class CommonReviewRecord:
    author_name: str
    review_text: str
    review_rating: int
    review_datetime_utc: str
    language: str


@dataclass
class GooglePlaceRevivewRecord(CommonReviewRecord):
    """
    Note: Google API uses UTC for time parameter.
    """


@dataclass
class OutScrapperReviewRecord(CommonReviewRecord):
    review_id: str
    google_id: str
    review_likes: int
    review_timestamp: str


@dataclass
class InHouseReviewRecord(CommonReviewRecord):
    pass


def is_filepath(string_or_list):
    given_type = type(string_or_list)
    if given_type == str:
        return True
    elif given_type == list:
        return False
    else:
        raise TypeError("a JSON filepath or a list should be given")


def convert_google_reviews_format_to_records(string_or_list_object):
    """
    It returns a list of ReviewRecord objects.
    """
    data = string_or_list_object

    if is_filepath(string_or_list_object):
        with open(string_or_list_object, "r") as f:
            data = json.load(f)
    review_records = []
    for d in data:
        review_records.append(
            GooglePlaceRevivewRecord(
                author_name=d["author_name"],
                review_text=d["text"],
                review_rating=d["rating"],
                review_datetime_utc=d["time"],
                language=d["language"],
            )
        )
    return review_records


def merge_all_reviews(review_records):
    """
    It merges all reviews in the list contains review records and then
    returns aggregated string for suitable for ChatGPT prompt.
    Future Note: This function can be useful for ChatGPT fine-tuning. For instance, I can add review rating before review's
    text body.
    """
    return "\n".join(map(lambda record: record.review_text, review_records))


def google_api_reviews_crawler(query, google_client):
    """
    The function takes a place name and returns five random reviews.
    If there are multiple places with same results it takes the first place
    in the query.

    This function is using Google's API.
    Args:
        query:
        google_client:

    Returns:

    """
    query_output = google_client.places(query)
    place_id = query_output["results"][0]["place_id"]
    first_place = google_client.place(place_id)
    reviews_raw = first_place["result"]["reviews"]
    return reviews_raw
