
import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import plotly.express as px

income_statement = None
balance_sheet = None
cash_flow = None
valuation_ratios = None
financial_ratios = None
dividends_and_splits = None
stock_data = None

def get_stock_info(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    return stock

def get_income_statement(stock_symbol: str) -> pd.DataFrame:
    """
    This is a tool that returns the quarterly income statement of a given stock ticker from yfinance.
    Args:
        stock_symbol: The stocker ticker or symbol to get data from.
    """
    # Fetch the stock data using yfinance
    # Create a yfinance ticker object
    #stock = yf.Ticker(stock_symbol)
    # Get quarterly financials
    income_statement = stock_symbol.quarterly_income_stmt
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
    #stock = yf.Ticker(stock_symbol)    
    # Get quarterly financials
    balance_sheet = stock_symbol.quarterly_balance_sheet
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
    #stock = yf.Ticker(stock_symbol)
        
    # Get quarterly financials
    cash_flow = stock_symbol.quarterly_cashflow
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

    


def get_valuation_measures(stock_symbol: str) -> pd.DataFrame:
    # Fetch the stock data using yfinance
    #stock = yf.Ticker(stock_symbol)
    info = stock_symbol.info

    

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
    valuation_df['Value'] = valuation_df['Value'].astype(str)

    return valuation_df


def get_financial_highlights(stock_symbol: str) -> pd.DataFrame:
    # Fetch the stock data using yfinance
    #stock = yf.Ticker(stock_symbol)
    info = stock_symbol.info

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

    financial_df['Value'] = financial_df['Value'].astype(str)

    return financial_df


def get_dividends_and_splits(stock_symbol: str) -> pd.DataFrame:
    # Fetch the stock data using yfinance
    #stock = yf.Ticker(stock_symbol)
    info = stock_symbol.info

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
    dividends_splits_data_df['Value'] = dividends_splits_data_df['Value'].astype(str)
    

    return dividends_splits_data_df


def get_dividend_details(stock_symbol: str) -> pd.DataFrame:    
    # Get historical dividend data
    #stock = yf.Ticker(stock_symbol)
    dividends = stock_symbol.dividends

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


def plot_stock_data(stock_symbol: str):
    ticker = yf.Ticker(stock_symbol)
    df = ticker.history(period='3y')  # returns a clean DataFrame
    fig = px.line(df, x=df.index, y="Close", title=f"{stock_symbol} Price")
    st.plotly_chart(fig)








