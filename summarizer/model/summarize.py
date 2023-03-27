import os
import openai
from enum import Enum

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.ORGANIZATION = "org-QnHenZwFez78ZbPcGeF5CFs2"


class SummarizeType(Enum):
    ALL = "all"
    POSITIVE = "positive"
    NEGATIVE = "negative"


def define_prompt(sum_type: SummarizeType):
    if sum_type == SummarizeType.ALL:
        return "Summarize these reviews:"
    elif sum_type == SummarizeType.POSITIVE:
        return (
            "Summarize the these reviews only using positive statements only:"
        )
    elif sum_type == SummarizeType.NEGATIVE:
        return (
            "Summarize the these reviews only using negative statements only:"
        )


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
        prompt=f"{define_prompt(sum_type)}\n\n{merged_reviews}",
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )

    return summary
