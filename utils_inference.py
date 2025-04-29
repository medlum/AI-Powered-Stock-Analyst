from huggingface_hub import InferenceClient
import streamlit as st
from together import Together

def initialize_inferenceclient(): 

    try:
        client = Together(api_key=st.session_state.access_token)
        return client
        
    except Exception as e:
        st.error(f"Error initializing Inference Client: {e}")
        st.stop()
        



#def initialize_inferenceclient(): 
#
#    try:
#        client = InferenceClient(
#	    provider="together",
#        api_key = st.session_state.access_token)
#        return client
#        
#    except Exception as e:
#        st.error(f"Error initializing Inference Client: {e}")
#        st.stop()
#        


model_list = [
                #"meta-llama/Llama-3.3-70B-Instruct",
                #"Qwen/Qwen2.5-72B-Instruct",
                #"deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
                "Qwen/Qwen2.5-72B-Instruct-Turbo"
                
            ]