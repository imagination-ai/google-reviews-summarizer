import os
import openai
from enum import Enum
from summarizer.crawler.crawl import (
    GOOGLE_REVIEWS_CLIENT,
    google_api_reviews_crawler,
    merge_all_reviews,
    convert_google_reviews_format_to_records,
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.ORGANIZATION = "org-QnHenZwFez78ZbPcGeF5CFs2"


class SummarizeType(Enum):
    ALL = "Summarize following reviews within one or two paragraphs:"
    POSITIVE = "Summarize the positive statements in the following reviews and turn into bullet points:"
    NEGATIVE = "Summarize the negative statements in the following reviews and turn into bullet points:"


def summarize_reviews(
    *,
    query: str,
    sum_type: SummarizeType,
    model: str,
    temperature: float,
    max_tokens: int,
    top_p: float,
    frequency_penalty: float,
    presence_penalty: float,
):
    crawled_reviews = google_api_reviews_crawler(
        query=query, google_client=GOOGLE_REVIEWS_CLIENT
    )
    merged_reviews = merge_all_reviews(
        convert_google_reviews_format_to_records(crawled_reviews)
    )
    summary = openai.Completion.create(
        model=model,
        prompt=f"{sum_type.value}\n\n{merged_reviews}",
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )

    return summary["choices"][0]["text"]
