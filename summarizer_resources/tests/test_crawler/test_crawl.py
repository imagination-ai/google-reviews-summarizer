import pytest
import mock
from summarizer.crawler.crawl import merge_all_reviews, get_photo_link

from summarizer.crawler.crawl import get_place_reviews
from summarizer.crawler.crawl import convert_google_reviews_format_to_records
from summarizer.crawler.crawl import GooglePlaceRevivewRecord


@pytest.fixture(scope="module")
def reviews_output():
    """Mock reviews output"""
    return {
        "result": {
            "reviews": {
                "author_name": "Stella White",
                "author_url": "https://www.google.com/maps/contrib/106622602129120648877/reviews",
                "language": "en",
                "original_language": "en",
                "profile_photo_url": "https://lh3.googleusercontent.com/a-/ACB-R5QkL3UsbasagZ3KmBshr3erfLLV1cViNdBbaygnUyg=s128-c0x00000000-cc-rp-mo",
                "rating": 5,
                "relative_time_description": "2 weeks ago",
                "text": "Excellent local coffee house, friendly and quick service! I come here regularly and it never disappoints. Highly recommend.",
                "time": 1678751000,
                "translated": False,
            }
        }
    }


@mock.patch("summarizer.crawler.crawl.get_place_all_info_from_google_api")
def test_get_place_reviews(mock_get_place_reviews, reviews_output):
    """
    Test condition: If the google-api returns correctly.
    Place method returns at least one place.
    """
    mock_get_place_reviews.return_value = reviews_output
    result = get_place_reviews("Saint Frank Coffee")
    assert result == reviews_output["result"]["reviews"]


def test_convert_google_reviews_format_to_records():
    review_records = convert_google_reviews_format_to_records(
        "summarizer_resources/tests/test_data/reviews.json"
    )
    assert len(review_records) == 5
    assert all(
        [isinstance(obj, GooglePlaceRevivewRecord) for obj in review_records]
    )


def test_merge_all_reviews():
    """
    The logic of this test, the length of the merged reviews has to always equal or
    bigger than the sum of the length of each review.
    """
    review_records = convert_google_reviews_format_to_records(
        "summarizer_resources/tests/test_data/reviews.json"
    )
    all_reviews = merge_all_reviews(review_records)
    length_of_the_all_reviews = sum(
        [len(record.review_text) for record in review_records]
    )
    assert len(all_reviews) >= length_of_the_all_reviews


@mock.patch("summarizer.crawler.crawl.requests.get")
def test_get_photo_link_success_case(mock_requests_get):
    mock_requests_get.return_value = mock.Mock(
        status_code=200, url="mock-test-url"
    )
    actual_url = get_photo_link("test-url")
    assert actual_url == "mock-test-url"
