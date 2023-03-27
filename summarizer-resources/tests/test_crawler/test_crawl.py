from summarizer.crawler.crawl import CLIENT, merge_all_reviews

# from summarizer.crawler.crawl import google_api_reviews_crawler
from summarizer.crawler.crawl import convert_google_reviews_format_to_records
from summarizer.crawler.crawl import GooglePlaceRevivewRecord


# def test_crawl():
# x = google_api_reviews_crawler('Saint Frank Coffee', CLIENT)
# TODO: But either way I should put some sleeping time to actual function.


def test_convert_google_reviews_format_to_records():
    review_records = convert_google_reviews_format_to_records(
        "summarizer-resources/tests/test_data/reviews.json"
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
        "summarizer-resources/tests/test_data/reviews.json"
    )
    all_reviews = merge_all_reviews(review_records)
    length_of_the_all_reviews = sum(
        [len(record.review_text) for record in review_records]
    )
    assert len(all_reviews) >= length_of_the_all_reviews
