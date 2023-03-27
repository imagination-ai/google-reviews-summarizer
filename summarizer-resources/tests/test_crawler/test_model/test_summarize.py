# from summarizer.crawler.crawl import convert_google_reviews_format_to_records, merge_all_reviews
from summarizer.model.summarize import (
    summarize_reviews,
    define_prompt,
    SummarizeType,
)


# def test_postive_summarization():
#     review_records = convert_google_reviews_format_to_records(
#         "summarizer-resources/tests/test_data/reviews.json"
#     )
#     all_reviews = merge_all_reviews(review_records)
#     summary = summarize_reviews(sum_type='positive', merged_reviews=all_reviews)
#     print(summary)


def test_define_prompt():
    assert define_prompt(SummarizeType.ALL) == "Summarize these reviews:"
