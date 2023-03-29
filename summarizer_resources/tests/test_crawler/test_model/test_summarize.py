# from summarizer.crawler.crawl import convert_google_reviews_format_to_records, merge_all_reviews
# from summarizer.model.summarize import (
#     summarize_reviews,
#     SummarizeType,
# )

#
# def test_summarization():
#     review_records = convert_google_reviews_format_to_records(
#         "summarizer_resources/tests/test_data/reviews.json"
#     )
#     all_reviews = merge_all_reviews(review_records)
#     summary = summarize_reviews(sum_type=SummarizeType.ALL, merged_reviews=all_reviews)
#     print(summary)
