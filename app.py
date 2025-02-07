import streamlit as st
from datetime import date, timedelta
from sentiment_analysis import check_news
import pandas as pd

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU

# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title("📊 Sentiment Check")

# User Inputs
start_date = st.date_input("Start Date", value=date.today() - timedelta(days=1))
end_date = st.date_input("End Date", value=date.today() - timedelta(days=1))
keywords = st.text_area("Enter Keywords (comma-separated)", value="SPX, QQQ, Fed, Nasdaq, Dow")

# Submit Button

if st.button("Check Sentiment"):
    # --- Process Inputs (Dummy Function) ---
    keywords_list = [k.strip() for k in keywords.split(",") if k.strip()]
    
    # Simulate long result output
    result = f"🔍 Searching for keywords: {keywords_list}\n"
    result += f"📅 Date Range: {start_date} to {end_date}\n\n"
    
    news_items = check_news(start_date, end_date, keywords_list)    
    
    if news_items:
        df = pd.DataFrame(news_items)
        df.columns = ['Title', 'Description', 'Sentiment', 'Score'] 
        
        # Apply conditional formatting
        def highlight_sentiment(row):
            color = '#DFFFD6' if row['Sentiment'] == 'positive' else '#FFEBEB'  # Light Green and Light Red
            return ['background-color: {}; color: black'.format(color)] * len(row)

        styled_df = df.style.apply(highlight_sentiment, axis=1).hide(axis="index")
        
        # st.dataframe(df.style.hide(axis="index"), use_container_width=True)
        st.markdown(styled_df.hide(axis="index").to_html(), unsafe_allow_html=True)

    else:
        st.info("No news items found for the given criteria.")


