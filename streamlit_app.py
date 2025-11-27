import streamlit as st
import pandas as pd
from utils_history import initialize_chat_history, initialize_session_state
from utils_inference import initialize_inferenceclient, model_list
from utils_markdown import display_md
from utils_stock import *
from utils_url import *
from sys_message import image_css, header
from utils_login import login_dialog, btn_css

st.set_page_config(page_title="AI Powered Stock Analyst",
                   layout="centered",
                   page_icon="💰",
                   initial_sidebar_state="expanded")


# Show login dialog if not authenticated
if not st.session_state.get("authenticated", False):
    login_dialog()

# Protected content
if st.session_state.get("authenticated", False):
    st.sidebar.success(f"Logged in as {st.session_state['user']}")

    # Initialize session state
    initialize_session_state()
    initialize_chat_history()

    # insert image 
    st.markdown(image_css, unsafe_allow_html=True)

    # initialize llm 
    client = initialize_inferenceclient()


    # -------------------- set up sidebar -------------------- #
    st.sidebar.subheader(":blue[AI-Powered Stock Analyst]")
    st.sidebar.image('cosmo.jpeg', width=80)
    st.sidebar.write(header)

    # select model
    model_select = st.sidebar.selectbox(":blue[AI model]", 
                            model_list,
                            index=0)

    # select stock exchange and extract stock symbol from csv
    exchange = st.sidebar.selectbox(":blue[Stock Exchange]", ['NYSE', 'SGX'], placeholder='Choose an stock exchange')

    if exchange == 'NYSE':
        df = pd.read_csv('./resource/NYSE.csv')
    elif exchange == 'SGX':
        df = pd.read_csv('./resource/SGX.csv')

    with st.sidebar:
        # select counter
        select_counter = st.selectbox(':blue[Stock Counter]', df["Name"], index=None, key='select_counter', placeholder='Choose a company')
        display_md.display('To clear chat history, simply unselect the stock counter.', font_size='12px', tag='p')

        st.markdown(btn_css, unsafe_allow_html=True)
        if st.button("Logout"):
            # Reset session state
            for key in ["authenticated", "user"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

        
    if select_counter:
        # filter stock symbol from company name
        stock_symbol = df.loc[df["Name"] == select_counter, "Symbol"].values[0]

        if stock_symbol:
            # get data from yfinance
            ticker = get_stock_info(stock_symbol)
            data = {
            'income_statement' : get_income_statement(ticker),
            'balance_sheet' : get_balance_sheet(ticker),
            'cash_flow' : get_cash_flow(ticker),
            'financial_ratios' : get_financial_highlights(ticker),
            'valuation_ratios' : get_valuation_measures(ticker),
            'dividends_and_splits' : get_dividends_and_splits(ticker),
            #'stock_data' : get_stock_data(stock_symbol),
            }
        
        # append data to llm message history 
        for key in data:
            if data[key] is not None:
                st.session_state.msg_history.append(
                        {"role": "system", "content": f"Here is the financial report for {stock_symbol} {select_counter}  : {data[key]}"})


        # -------------------- news retrieval  -------------------- #

        # build brave query using company and stock symbol 
        query = build_query(select_counter, stock_symbol)
        # get results with query 
        search_results = get_url(select_counter)

        # set count to extract 5 news article
        success_count = 0
        max_success = 5

        with st.spinner(f"Retrieving news on {select_counter}..."):

            for index, news in enumerate(search_results['results']):
                url = news.get('url', '')
                title = news.get('title', 'No Title')
                age = news.get('age', 'No age')
                # extract contents with url using newspaper3k
                content = extract_article_text(url)
                #  continue with loop, if error message 
                if content.startswith("❌") or content.startswith("⚠️"):
                    continue

                # display article title and date
                display_md.display(title, color="#040404")
                display_md.display(age, font_size='14px', tag='p', italic=True)

                # append news to news history
                st.session_state.news_history.append(
                {"role": "system", "content": f"here is one of the news : {content}"})

                # llm to summarize news in response
                placeholder = st.empty()
                stream = client.chat.completions.create(
                    model=model_select,
                    messages=st.session_state.news_history,
                    temperature=0.2,
                    max_tokens=5524,
                    top_p=0.7,
                    stream=True,
                    )

                # Initialize an empty string to collect the streamed content
                collected_response = ""
                
                # Stream the response and update the placeholder in real-time
                #for chunk in stream:
                #    collected_response += chunk.choices[0].delta.content
                #    placeholder.write(collected_response.replace("{", " ").replace("}", " "))
                
                for chunk in stream:
                    if chunk.output_text:
                        collected_response += chunk.output_text
                        placeholder.write(collected_response)

                # append summarize news from llm to message history
                st.session_state.msg_history.append({"role": "system", "content": f"{collected_response}"})

                # show news url and icon at each news summary
                col1, col2 = st.columns([0.4,10], gap='small', vertical_alignment="center")            
                col1.image(news['meta_url']['favicon'], width=20)
                col2.markdown(
                    f'<p style="font-size:14px; color:blue;"><a href="{news['url']}" target="_blank" style="text-decoration: none;">Read more...</a></p>',
                    unsafe_allow_html=True)
                
                # remove news history after each loop
                st.session_state.news_history[1:] = []    

                success_count += 1
                if success_count > max_success:
                    break

        st.divider()
                    

        # -------------------- news retrieval  -------------------- #

        with st.spinner("Analyzing Stock Performance..."):

            placeholder = st.empty()

            stream = client.responses.create(
                model=model_select,
                messages=st.session_state.msg_history,
                temperature=0.2,
                max_output_tokens=5524,
                top_p=0.7,
                stream=True,
            )

            collected_response = ""

            for chunk in stream:
                if chunk.output_text:
                    collected_response += chunk.output_text
                    placeholder.write(collected_response)

            # Add assistant final reply to history
            st.session_state.msg_history.append({
                "role": "assistant",
                "content": collected_response
            })

            
            # llm to analyze and recommend stock with yfinance data and news summary
#            placeholder = st.empty()
#            stream = client.chat.completions.create(
#                model=model_select,
#                messages=st.session_state.msg_history,
#                temperature=0.2,
#                max_tokens=5524,
#                top_p=0.7,
#                stream=True,
#                )
#
#            # Initialize an empty string to collect the streamed content
#            collected_response = ""
#            
#            # Stream the response and update the placeholder in real-time
#            for chunk in stream:
#                collected_response += chunk.choices[0].delta.content
#                placeholder.write(collected_response.replace("{", " ").replace("}", " "))
#            
#            # Add the assistant's response to the conversation history
#            st.session_state.msg_history.append(
#                {"role": "assistant", "content": collected_response})
            
            st.divider()
            
            # -------------------- display financial data from yfinance  -------------------- #
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

                with tab7:
                    plot_stock_data(stock_symbol)

    else:
        # clear all history when stock counter selectbox change
        st.session_state.msg_history[1:] = []
        st.session_state.news_history[1:] = []


    
    #for msg in st.session_state.msg_history:
    #    if msg['role'] != "system":
    #        st.chat_message(msg["role"]).write(msg["content"])
            
    #if user_input := (st.chat_input("Ask a question...") or select_counter):