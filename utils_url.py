
import requests
import json
from newspaper import Article
from urllib.parse import urlparse
import streamlit as st
from utils_markdown import display_md

def build_query(company: str, ticker: str = "") -> str:
    keywords = [
    "forecast", "guidance", "estimates",
    "sales", "earnings", "profit", "revenue", "valuation", "growth", "AI",
    "regulatory", "debt",
    "competition", "M&A", "supply chain", "expansion", "layoffs", "demand",
    "executive changes", "product launch", "cash flow"
    ]


    # Build company part (no quotes)
    company_query = f"({company}" + (f" OR {ticker}" if ticker else "") + ")"

    # Join keywords with OR, no quotes
    keyword_clause = " OR ".join(keywords)

    # Final query
    query = f"{company_query} AND ({keyword_clause})"
    return query



# Known paywalled domains (you can expand this)
PAYWALLED_DOMAINS = {'wsj.com', 'ft.com', 'bloomberg.com', 'nytimes.com', 'economist.com'}

def get_url(query) -> json:
    """
    This tool returns the search result of a Brave News API call for company financial outlook news,
    using a custom Brave Goggle to improve result quality.
    Returns:
        The search results in JSON.
    """
    # Replace "Apple Inc" with your dynamic input elsewhere in the app
    #query = (
    #    f'{company} AND '
    #    '(outlook OR forecast OR guidance OR estimates OR "future performance" OR '
    #    '"sales")'
    #)

    #query = (
    #    f'{company} AND '
    #    '(outlook OR forecast OR guidance OR estimates OR "future performance" OR '
    #    '"iPhone sales" OR "macroeconomic conditions" OR inflation OR "interest rates" OR '
    #    '"supply chain" OR "AI strategy" OR China")'
    #)

    encoded_query = requests.utils.quote(query)

    # Use the user-provided Gist for Brave Goggles
    raw_goggle_url = (
        "https://gist.githubusercontent.com/medlum/acd4fcb37229a7f589510794a29eeb1d/raw/"
        "8f2cffa544692eb0f69a763c5b9c04fbefbe4bff/trusted-financial-news.goggle"
        )
    encoded_goggle_url = requests.utils.quote(raw_goggle_url)

    url = (
        f"https://api.search.brave.com/res/v1/news/search"
        f"?q={encoded_query}&count=20&freshness=p30d"
        f"&goggles={encoded_goggle_url}"
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "Referer": "https://www.google.com",
        "X-Subscription-Token": "BSANRhMz7xnB_dIA1nzDwO2uaw3cpVA"
    }

    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    return response.json()


def is_paywalled_domain(url: str) -> bool:
    domain = urlparse(url).netloc
    return any(pw_domain in domain for pw_domain in PAYWALLED_DOMAINS)

def extract_article_text(url: str) -> str:
    """
    Uses newspaper3k to extract clean article text.
    Skips paywalled domains and returns fallback on failure.
    """
    if is_paywalled_domain(url):
        return f"⚠️ Skipping paywalled article: {url}"
    
    try:
        article = Article(url)
        article.download()
        article.parse()

        text = article.text.strip()

        # If the article text is too short, possibly not parsed correctly
        if len(text) < 200:
            return "⚠️ Article content too short or not accessible."

        return text

    except Exception as e:
        return f"❌ Failed to extract article: {str(e)}"

# Main logic
#company = "advanced micro devices"
#search_results = get_url(company)
#st.write(search_results)
#
#success_count = 0
#max_success = 5
#
#for index, news in enumerate(search_results['results']):
#    url = news.get('url', '')
#    title = news.get('title', 'No Title')
#    age = news.get('age', 'No age')
#
#    content = extract_article_text(url)
#
#    if content.startswith("❌") or content.startswith("⚠️"):
#        continue
#    
#    #st.markdown(news["url"])
#    #st.markdown(f"### [{title}]({url})")
#    st.write(f":blue[{title}]")
#    display_md.display(age, font_size='14px', tag='p')
#   
#    st.write(content)
#
#    success_count += 1
#    if success_count >= max_success:
#        break
