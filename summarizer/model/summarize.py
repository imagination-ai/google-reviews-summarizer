import os
import openai
from enum import Enum

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.ORGANIZATION = "org-QnHenZwFez78ZbPcGeF5CFs2"


class SummarizeType(Enum):
    ALL = "Summarize following reviews within one or two paragraphs:"
    POSITIVE = "Summarize the positive statements in the following reviews and turn into bullet points:"
    NEGATIVE = "Summarize the negative statements in the following reviews and turn into bullet points:"


def summarize_reviews(
    sum_type: SummarizeType,
    merged_reviews: str,
    model="text-davinci-003",
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
):

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
