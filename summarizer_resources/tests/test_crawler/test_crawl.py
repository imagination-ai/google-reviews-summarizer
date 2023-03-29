import pytest

from summarizer.crawler.crawl import merge_all_reviews

from summarizer.crawler.crawl import google_api_reviews_crawler
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


@pytest.fixture(scope="module")
def mock_google_client(reviews_output):
    """Mock Google API client object for testing"""

    class MockClient:
        def __init__(self, mock_key):
            self.mock_key = mock_key

        def places(self, query):
            return query_output

        def place(self, place_id):
            return reviews_output

    # Mock places output
    query_output = {
        "html_attributions": [],
        "results": [
            {
                "business_status": "OPERATIONAL",
                "place_id": "ChIJlzvceNUadmsmK26khe0U",
            }
        ],
        "status": "OK",
    }

    return MockClient("Mock-Key")


def test_google_api_reviews_crawler(mock_google_client, reviews_output):
    """
    Test condition: If the google-api returns correctly.
    Place method returns at least one place.
    """
    expected_output = reviews_output["result"]["reviews"]
    assert (
        google_api_reviews_crawler("Saint Frank Coffee", mock_google_client)
        == expected_output
    )


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
