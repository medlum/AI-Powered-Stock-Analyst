
import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import requests
import json
from markdownify import markdownify
from requests.exceptions import RequestException
import re
from sys_message import *

class DisplayMarkdown:
    def __init__(self, color="#737578", font_size="16px", tag="h2", text_align="left"):
        self.color = color
        self.font_size = font_size
        self.tag = tag
        self.text_align = text_align

    def display(self, text, color=None, font_size=None, tag=None, text_align=None):
        # Use the provided color, font_size, tag, and text_align if given, otherwise use the defaults
        color = color if color is not None else self.color
        font_size = font_size if font_size is not None else self.font_size
        tag = tag if tag is not None else self.tag
        text_align = text_align if text_align is not None else self.text_align

        markdown_html = f"""
        <{tag} style='color:{color}; font-size: {font_size}; text-align: {text_align};'>{text}</{tag}>
        """
        st.markdown(markdown_html, unsafe_allow_html=True)

display_md = DisplayMarkdown()


income_statement = None
balance_sheet = None
cash_flow = None
valuation_ratios = None
financial_ratios = None
dividends_and_splits = None
stock_data = None


def get_income_statement(stock_symbol: str) -> pd.DataFrame:
    """
    This is a tool that returns the quarterly income statement of a given stock ticker from yfinance.
    Args:
        stock_symbol: The stocker ticker or symbol to get data from.
    """
    # Fetch the stock data using yfinance
    # Create a yfinance ticker object
    stock = yf.Ticker(stock_symbol)
    # Get quarterly financials
    income_statement = stock.quarterly_income_stmt
    if income_statement.empty:
        st.error(f"No income statement found for {stock_symbol}.")
        return None
    
    income_statement.columns = pd.to_datetime(income_statement.columns).strftime('%Y-%m-%d')
    return income_statement


def get_balance_sheet(stock_symbol: str) -> pd.DataFrame:
    """
    This is a tool that returns the quarterly balance sheet statement of a given stock ticker from yfinance.
    Args:
        stock_symbol: The stocker ticker or symbol to get data from.
    """
    # Fetch the stock data using yfinance
    # Create a yfinance ticker object
    stock = yf.Ticker(stock_symbol)    
    # Get quarterly financials
    balance_sheet = stock.quarterly_balance_sheet
    if balance_sheet.empty:
        st.error(f"No balance sheet statement found for {stock_symbol}.")
        return None
    
    balance_sheet.columns = pd.to_datetime(balance_sheet.columns).strftime('%Y-%m-%d')
    return balance_sheet


def get_cash_flow(stock_symbol: str) -> pd.DataFrame:
    """
    This is a tool that returns the quarterly cash flow statement of a given stock ticker from yfinance.
    Args:
        stock_symbol: The stocker ticker or symbol to get data from.
    """
    # Fetch the stock data using yfinance
    # Create a yfinance ticker object
    stock = yf.Ticker(stock_symbol)
        
    # Get quarterly financials
    cash_flow = stock.quarterly_cashflow
    if cash_flow.empty:
        st.error(f"No cash flow found for {stock_symbol}.")
        return None

    cash_flow.columns = pd.to_datetime(cash_flow.columns).strftime('%Y-%m-%d')
    return cash_flow



def get_stock_data(stock_symbol: str) -> pd.DataFrame:
    """
    This is a tool that returns the stock data of a given stock ticker from yfinance.
    It returns the stock data of the specific columns and the stock symbol.

    Args:
        stock_symbol: The stocker ticker or symbol to get data from.
    """
    try:
        # Calculate the start date (one year ago from today)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)

        # Download the historical data
        stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

        # Check if the data is empty
        if stock_data.empty:
            st.error(f"No data found for {stock_symbol} between {start_date.date()} and {end_date.date()}.")
            return None

        return stock_data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def plot_stock_data(stock_symbol:str) -> any:
    """
    This is a tool display a stock price chart.

    Args:
        stock_symbol: The stock symbol of the company
    """
    iframe_url = f"https://macrotrends.net/assets/php/stock_price_history.php?t={stock_symbol}"

    # Display in Streamlit
    st.components.v1.iframe(iframe_url, 
                            width=700, 
                            height=800, 
                            scrolling=True)
    


def get_valuation_measures(stock_symbol: str) -> pd.DataFrame:
    # Fetch the stock data using yfinance
    stock = yf.Ticker(stock_symbol)
    info = stock.info

    

    # Extract valuation-related data
    valuation_measures = {
            "Market cap": info.get("marketCap"),
            "Enterprise value": info.get("enterpriseValue"),
            "Trailing P/E": round(info.get("trailingPE"), 3) if isinstance(info.get("trailingPE"), (int, float)) else None,
            "Forward P/E": round(info.get("forwardPE"), 3) if isinstance(info.get("forwardPE"), (int, float)) else None,
            "PEG ratio (5-yr expected)": round(info.get("pegRatio"), 3) if isinstance(info.get("pegRatio"), (int, float)) else None,
            "Price/sales": round(info.get("priceToSalesTrailing12Months"), 3) if isinstance(info.get("priceToSalesTrailing12Months"), (int, float)) else None,
            "Price/book": round(info.get("priceToBook"), 3) if isinstance(info.get("priceToBook"), (int, float)) else None,
            "Enterprise value/revenue": info.get("enterpriseToRevenue"),
            "Enterprise value/EBITDA": info.get("enterpriseToEbitda"),
        }

    # Format large numbers (e.g., Market cap, Enterprise value) into billions
    for key in ["Market cap", "Enterprise value"]:
        if valuation_measures[key]:
            valuation_measures[key] = f"{valuation_measures[key] / 1e9:.2f}B"

    # Convert the dictionary to a DataFrame
    valuation_df = pd.DataFrame(list(valuation_measures.items()), columns=['Measure', 'Value'])

    return valuation_df


def get_financial_highlights(stock_symbol: str) -> pd.DataFrame:
    # Fetch the stock data using yfinance
    stock = yf.Ticker(stock_symbol)
    info = stock.info

    # Extract financial highlights
    financial_highlights = {
        "Total revenue": info.get("totalRevenue"),
        "Gross profit": info.get("grossProfits"),
        "EBITDA": info.get("ebitda"),
        "Net income": info.get("netIncomeToCommon"),
        "Total debt": info.get("totalDebt"),
        "Current debt": info.get("currentDebt"),
        "Total cash": info.get("totalCash"),
        "Free cash flow": info.get("freeCashflow"),
        "Operating margin": round(info.get("operatingMargins"), 3) if isinstance(info.get("operatingMargins"), (int, float)) else None,
        "Profit margin": round(info.get("profitMargins"), 3) if isinstance(info.get("profitMargins"), (int, float)) else None,
        "Return on equity %": round(info.get("returnOnEquity") * 100, 2) if isinstance(info.get("returnOnEquity"), (int, float)) else None,
        "Return on assets %": round(info.get("returnOnAssets") * 100, 2) if isinstance(info.get("returnOnAssets"), (int, float)) else None,
    }

    # Format large monetary values into billions
    for key in ["Total revenue", "Gross profit", "EBITDA", "Net income", "Total debt", "Current debt", "Total cash", "Free cash flow"]:
        if financial_highlights[key]:
            financial_highlights[key] = f"{financial_highlights[key] / 1e9:.2f}B"

    # Convert the dictionary to a DataFrame
    financial_df = pd.DataFrame(list(financial_highlights.items()), columns=["Highlight", "Value"])

    return financial_df


def get_dividends_and_splits(stock_symbol: str) -> pd.DataFrame:
    # Fetch the stock data using yfinance
    stock = yf.Ticker(stock_symbol)
    info = stock.info

    dividends_splits_data = {
        "Forward annual dividend rate": info.get("dividendRate"),
        "Forward annual dividend yield %": round(info.get("dividendYield") * 100,2) if info.get("dividendYield") else None,
        "Trailing annual dividend rate": info.get("trailingAnnualDividendRate"),
        "Trailing annual dividend yield %": round(info.get("trailingAnnualDividendYield") * 100,2) if info.get("trailingAnnualDividendYield") else None,
        "5-year average dividend yield": info.get("fiveYearAvgDividendYield"),
        "Payout ratio %": info.get("payoutRatio" * 100) if info.get("payoutRatio") else None,
        "Dividend date": pd.to_datetime(info.get("dividendDate"), unit='s').strftime('%Y-%m-%d') if info.get("dividendDate") else None,
        "Ex-dividend date": pd.to_datetime(info.get("exDividendDate"), unit='s').strftime('%Y-%m-%d') if info.get("exDividendDate") else None,
        "Last split factor": info.get("lastSplitFactor"),
        "Last split date": pd.to_datetime(info.get("lastSplitDate"), unit='s').strftime('%Y-%m-%d') if info.get("lastSplitDate") else None,
    }

    dividends_splits_data_df = pd.DataFrame(list(dividends_splits_data.items()), columns=['Measure', 'Value'])

    return dividends_splits_data_df


def get_dividend_details(stock_symbol: str) -> pd.DataFrame:    
    # Get historical dividend data
    stock = yf.Ticker(stock_symbol)
    dividends = stock.dividends

    if dividends.empty:
        return None

    # Determine payout frequency and total dividends
    dividends_per_year = dividends.resample('YE').count()  # Count dividends each year
    total_dividends_per_year = dividends.resample('YE').sum()  # Sum dividends each year

    # Extract most recent year's data
    latest_year = dividends_per_year.index[-1].year
    payouts_last_year = dividends_per_year.iloc[-1]
    total_dividend_last_year = total_dividends_per_year.iloc[-1]

    # Determine payout frequency
    payout_frequency = "Quarterly" if payouts_last_year == 4 else (
        "Semi-Annually" if payouts_last_year == 2 else (
            "Annually" if payouts_last_year == 1 else f"{payouts_last_year} times/year"
        )
    )

    # Convert the index to only dates
    dividends_last_year = dividends[dividends.index.year == latest_year].copy()
    dividends_last_year.index = dividends_last_year.index.date

    # Convert to dictionary and format as a string
    dividends_last_year_dict = {str(date): value for date, value in dividends_last_year.to_dict().items()}
    dividends_last_year_string = ", ".join(f"{date}: {value}" for date, value in dividends_last_year_dict.items())

    # Prepare data for the DataFrame
    data = [
        {"Metric": "Payout frequency", "Value": payout_frequency},
        {"Metric": "Total dividend last year", "Value": round(total_dividend_last_year, 3)},
        {"Metric": "Dividends last year", "Value": dividends_last_year_string},
    ]
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df


def plot_stock_data(stock_symbol:str) -> any:
    """
    This is a tool display a stock price chart.

    Args:
        stock_symbol: The stock symbol of the company
    """
    iframe_url = f"https://macrotrends.net/assets/php/stock_price_history.php?t={stock_symbol}"

    # Display in Streamlit
    st.components.v1.iframe(iframe_url, 
                            width=700, 
                            height=800, 
                            scrolling=False)


def initialize_session_state():
    """Initialize session state variables if they do not exist."""
    if 'news_history' not in st.session_state:
        st.session_state.news_history = []
    if 'msg_history' not in st.session_state:
        st.session_state.msg_history = []

def initialize_chat_history():
    """Set up system messages for news summarization and stock analysis."""
    st.session_state.news_history.append({"role": "system", "content": system_news_message})
    st.session_state.msg_history.append({"role": "system", "content": system_analysis_message})



def get_url(query:str) -> json:
    """
    This tool returns the search result of an api call to a client url. 
    Args:
        query: The query parameter - q in the api call.   
    Returns:
        The search results in json.

    """
    url = f"https://api.search.brave.com/res/v1/news/search?q={query}&count=5&country=us&search_lang=en&spellcheck=1"
    
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": "BSANRhMz7xnB_dIA1nzDwO2uaw3cpVA"
    }
    
    response = requests.get(url, headers=headers)
    
    return response.json()


def visit_webpage(url: str) -> str:
    """Visits a webpage at the given URL and returns its content as a markdown string.
    Args:
        url: The URL of the webpage to visit.
    Returns:
        The content of the webpage converted to Markdown, or an error message if the request fails.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Convert the HTML content to Markdown
        markdown_content = markdownify(response.text,  strip=["nav", "aside", "footer"]).strip()

        # Remove multiple line breaks
        markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

        return markdown_content

    except RequestException as e:
        return f"Error fetching the webpage: {str(e)}"
    
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

query = "oracle"
search_results = get_url(query=query)

for index, news in enumerate(search_results['results']):
    print("COUNT: ", news['url'])
    print(visit_webpage(news['url']))

url = "https://apnews.com/article/trump-eu-tariffs-countermeasures-806a3b9bcc9cd4e45817e672d95f0070"
content = (visit_webpage(url))
print(content)

#def get_analyst_price_target(stock_symbol: str) -> pd.DataFrame:    
#    stock = yf.Ticker(stock_symbol)
#    data = stock.get_analyst_price_target
#    if data.empty:
#        return None
#    
#    return data
#
#
#def fetch_earnings_calendar(stock_symbol: str) -> pd.DataFrame:    
#    stock = yf.Ticker(stock_symbol)
#    data = stock.get_calendar()
#    if data.empty:
#        return None
#    return data
#
#
#
#def fetch_recommendations(stock_symbol: str) -> pd.DataFrame:   
#    stock = yf.Ticker(stock_symbol) 
#    data = stock.get_recommendations_summary()
#    if data.empty:
#        return None
#    return data
#
#def fetch_upgrades_downgrades(stock_symbol: str) -> pd.DataFrame:    
#    stock = yf.Ticker(stock_symbol)
#    data = stock.get_upgrades_downgrades()
#    if data.empty:
#        return None
#    return data
#



