import logging

from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel

from summarizer.model.summarize import SummarizeType, summarize_reviews
from summarizer.crawler.crawl import GOOGLE_REVIEWS_CLIENT
from summarizer.crawler.crawl import google_api_reviews_crawler
from summarizer.utils.customized_logging import configure_logging
from summarizer.config import settings

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
v1 = FastAPI()

tags_metadata = [
    {"name": "Index", "description": "Index page for the project"},
    {
        "name": "Google-Crawl",
        "description": "Google API Crawler that I use in the project",
        "externalDocs": {
            "description": "The doc of Google API",
            "url": "https://developers.google.com/maps/documentation/places/web-service/details",
        },
    },
    {
        "name": "OpenAI-Summarizer",
        "description": "A simple summarizer that uses OPENAI API",
    },
    {
        "name": "Summarizer",
        "description": "A simple summarizer that only takes query and what type of summary which user wants",
    },
]


class CrawlArgs(BaseModel):
    sum_type: SummarizeType
    model: str = "text-davinci-003"
    temperature: float = Query(0.7, le=2.0, ge=0)
    max_tokens: int = 256
    top_p: float = 1.0
    frequency_penalty: float = 0
    presence_penalty: float = 0


# Index page
@app.get("/", tags=["Index"])
async def index():
    message = (
        "Google Reviews Summarizer is working! See the doc at" "/api/v1/docs"
    )
    return {"success": True, "message": message}


# The endpoint for Google API Crawler
@v1.get("/google-crawl-reviews", tags=["Google-Crawl"])
async def fetch_reviews_with_google_api(query: str):
    logger.info("Crawler is just starting working.")
    return google_api_reviews_crawler(query, GOOGLE_REVIEWS_CLIENT)


# The endpoint for bring reviews summary directly
@v1.get("/openai-summarizer", tags=["Summarizer"])
async def summarize_this_reviews_via_openai(
    query: str, parameters: CrawlArgs = Depends()
):
    return summarize_reviews(query=query, **parameters.dict())


app.mount(settings.API_BASE_URL, v1)

if __name__ == "__main__":
    import uvicorn

    logger.warning("Friendly Warning: Local Development...")
    uvicorn.run(
        "summarizer.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
        workers=1,
    )
