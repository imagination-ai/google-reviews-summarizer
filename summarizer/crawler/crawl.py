import googlemaps
import os
from dataclasses import dataclass
import json
import requests
from functools import lru_cache

GOOGLE_REVIEWS_API_KEY = os.environ["GOOGLE_REVIEWS_API_KEY"]
GOOGLE_REVIEWS_CLIENT = googlemaps.Client(key=GOOGLE_REVIEWS_API_KEY)


@dataclass
class PlaceGeneralRecords:
    average_rating: float
    price_level: str
    place_type: str
    photo_reference: str
    wheelchair_accessible_entrance: str
    website: str


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


def get_photo_link(
    photo_reference,
    max_height=800,
    max_width=600,
    google_api_key=GOOGLE_REVIEWS_API_KEY,
):
    _ = "https://maps.googleapis.com/maps/api/place/photo?"
    query = f"{_}maxheight={max_height}&maxwidth={max_width}&photoreference={photo_reference}&key={google_api_key}"
    r = requests.get(query)
    if r.status_code == 200:
        return r.url
    else:
        print(f"Critical Error in get_photo_link function:{r.status_code}")


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


@lru_cache
def get_place_all_info_from_google_api(query):
    query_output = GOOGLE_REVIEWS_CLIENT.places(query)
    place_id = query_output["results"][0]["place_id"]
    first_place = GOOGLE_REVIEWS_CLIENT.place(place_id)
    return first_place


def get_place_reviews(query):
    """
    The function takes a place name and returns five random reviews.
    If there are multiple places with same results it takes the first place
    in the query.

    This function is using Google's API.
    Args:

    Returns:

    """
    first_place = get_place_all_info_from_google_api(query)
    result = first_place["result"]
    reviews_raw = result["reviews"]
    return reviews_raw


def get_place_general_information(query):
    # general information about place (e.g., price level)

    first_place = get_place_all_info_from_google_api(query)
    result = first_place["result"]
    average_rating = result["rating"]
    price_level = result["price_level"] * "$"
    place_type = result["types"][0].replace("_", " ").title()
    photo_reference = result["photos"][0]["photo_reference"]

    if result["wheelchair_accessible_entrance"] is True:
        wheelchair_accessible_entrance = "Wheelchair accessible"
    else:
        wheelchair_accessible_entrance = "NA"

    if result["website"]:
        website = result["website"]
    else:
        website = "NA"

    general_records = PlaceGeneralRecords(
        average_rating,
        price_level,
        place_type,
        photo_reference,
        wheelchair_accessible_entrance,
        website,
    )
    return general_records
