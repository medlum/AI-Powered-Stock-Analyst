import streamlit as st
import pandas as pd
import yfinance as yf
from huggingface_hub import InferenceClient
from utils import *

st.set_page_config(page_title="AI Powered Stock Analyst",
                   layout="centered",
                   page_icon="💰",
                   initial_sidebar_state="expanded")

income_statement = None
balance_sheet = None
cash_flow = None
valuation_ratios = None
financial_ratios = None
dividends_and_splits = None
stock_data = None


# Initialize session state
initialize_session_state()
initialize_chat_history()

client = InferenceClient(token=st.secrets.api_keys.huggingfacehub_api_token)

st.sidebar.subheader(":blue[AI-Powered Stock Analyst]")
st.sidebar.write(header)
# set LLM model
model_select = st.sidebar.selectbox(":blue[AI model]", 
                        ["Qwen/Qwen2.5-72B-Instruct",
                            "Qwen/Qwen2.5-Coder-32B-Instruct",
                            "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
                            "Qwen/QwQ-32B-Preview",
                            "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
                            "meta-llama/Llama-3.3-70B-Instruct",
                            "meta-llama/Llama-3.1-8B-Instruct"],
                        index=5,
                        )

exchange = st.sidebar.selectbox(":blue[Stock Exchange]", ['NYSE', 'SGX'], placeholder='Choose an stock exchange')

if exchange == 'NYSE':
    df = pd.read_csv('./resource/NYSE.csv')

elif exchange == 'SGX':
    df = pd.read_csv('./resource/SGX.csv')

with st.sidebar:
    
    select_counter = st.selectbox(':blue[Stock Counter]', df["Name"], index=None, key='select_counter', placeholder='Choose a company')
    display_md.display('To clear chat history, simply unselect the stock counter.', font_size='14px', tag='p')

if select_counter:

    stock_symbol = df.loc[df["Name"] == select_counter, "Symbol"].values[0]
    if stock_symbol:
        data = {
        'income_statement' : get_income_statement(stock_symbol),
        'balance_sheet' : get_balance_sheet(stock_symbol),
        'cash_flow' : get_cash_flow(stock_symbol),
        'financial_ratios' : get_financial_highlights(stock_symbol),
        'valuation_ratios' : get_valuation_measures(stock_symbol),
        'dividends_and_splits' : get_dividends_and_splits(stock_symbol),
        'stock_data' : get_stock_data(stock_symbol),
        }
    
    for key in data:
        if data[key] is not None:
            st.session_state.msg_history.append(
                    {"role": "system", "content": f"Here is the financial report for {stock_symbol} {select_counter}  : {data[key]}"})

    search_results = get_url(select_counter)

    for index, news in enumerate(search_results['results']):

        with st.spinner(f"Retrieving news..."):

            st.session_state.news_history.append(
            {"role": "system", "content": f"here is one of the news : {visit_webpage(news['url'])}"})

            with st.empty():
                        # Stream the response

                stream = client.chat_completion(
                    model="Qwen/Qwen2.5-Coder-32B-Instruct",
                    messages=st.session_state.news_history,
                    temperature=0.1,
                    max_tokens=4524,
                    top_p=0.7,
                    stream=True,)

                # Initialize an empty string to collect the streamed content
                collected_response = ""
                
                # Stream the response and update the placeholder in real-time
                for chunk in stream:
                    if 'delta' in chunk.choices[0] and 'content' in chunk.choices[0].delta:
                        collected_response += chunk.choices[0].delta.content
                        with st.chat_message("assistant"):
                            st.write(collected_response)
                            col1, col2 = st.columns([0.4,10], gap='small', vertical_alignment="center")            
                            col1.image(news['meta_url']['favicon'], width=20)
                            col2.markdown(
                                f'<p style="font-size:14px; color:blue;"><a href="{news['url']}" target="_blank" style="text-decoration: none;">Read more...</a></p>',
                                unsafe_allow_html=True)
                st.session_state.msg_history.append({"role": "system", "content": f"{collected_response}"})

        st.session_state.news_history[1:] = []    
                
else:
    st.session_state.msg_history[1:] = []
    st.session_state.news_history[1:] = []


for msg in st.session_state.msg_history:
    if msg['role'] != "system":
        st.chat_message(msg["role"]).write(msg["content"])
        
if user_input := (st.chat_input("Ask a question...") or select_counter):

    with st.spinner("Analyzing Stock Performance..."):

        if user_input != select_counter:
            # Append the user's input to the msg_history
            st.session_state.msg_history.append(
                {"role": "user", "content": user_input})

            # write current chat on UI
            if user_input != select_counter:
                with st.chat_message("user"):
                    st.write(user_input)

            # Create a placeholder for the streaming response 
        with st.empty():
                    # Stream the response

            stream = client.chat_completion(
                model=model_select,
                messages=st.session_state.msg_history,
                temperature=0.6,
                max_tokens=4524,
                top_p=0.7,
                stream=True,)

            # Initialize an empty string to collect the streamed content
            collected_response = ""

            # Stream the response and update the placeholder in real-time
            for chunk in stream:
                if 'delta' in chunk.choices[0] and 'content' in chunk.choices[0].delta:
                    collected_response += chunk.choices[0].delta.content
                    with st.chat_message("assistant"):
                        st.write(collected_response)
        
        # Add the assistant's response to the conversation history
        st.session_state.msg_history.append(
            {"role": "assistant", "content": collected_response})

        with st.container(border=False):

            tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Income statement", "Balance sheet", "Cash flow", "Ratios", "Valuations", "Dividends", "Stock Price"])
            
            if data['income_statement'] is not None:
               tab1.dataframe(data['income_statement'])
            
            if data['balance_sheet'] is not None:
                tab2.dataframe(data['balance_sheet'])
            
            if  data['cash_flow'] is not None:
                tab3.dataframe(data['cash_flow'])
              
            if data['financial_ratios'] is not None:
                tab4.dataframe(data['financial_ratios'])
            
            if data['valuation_ratios'] is not None:
                 tab5.dataframe(data['valuation_ratios'])
               
            if data['dividends_and_splits'] is not None:
                tab6.dataframe(data['dividends_and_splits'])

            if data['stock_data'] is not None:
                with tab7:
                    plot_stock_data(stock_symbol)