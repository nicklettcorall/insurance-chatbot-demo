# --- insurance_products.csv (Sample content) ---
# Plan Name,Insurer,Plan Type,Key Features,Suitable For,Premium Range
# Singlife Shield Plan 2,Singlife,Health Insurance,Private hospital coverage with MediSave support,General Hospitalization,$1000/year
# Singlife Health Plus,Singlife,Health Rider,Covers deductible and co-insurance portion,Hospital Enhancer,$300/year
# FWD Big 3 Critical Illness,FWD,Critical Illness,Covers Cancer, Heart Attack, Stroke,CI Needs,$500/year
# China Taiping i-Save,China Taiping,Endowment,Savings plan with guaranteed returns,Education Planning,$1500/year
# FWD Future First,FWD,Endowment,Endowment plan with flexible maturity,General Savings,$1200/year
# China Taiping i-Secure Retirement,China Taiping,Retirement,Regular payout after retirement age,Retirement Planning,$1800/year

# --- app.py ---

import streamlit as st
import openai
from utils import load_products, openai_answer, analyze_client_gaps

st.set_page_config(page_title="Insurance Advisor Bot", layout="centered")

st.title("🤖 Insurance Advisor Chatbot")
openai.api_key = st.text_input("Enter your OpenAI API Key", type="password")

# Load product data
products_df = load_products()
product_text = products_df.to_string(index=False)

# Chat mode
st.subheader("💬 Chat with Ray")
user_input = st.text_input("Ask me anything about insurance...")
if st.button("Send") and user_input:
    system_prompt = "You are an intelligent insurance advisor. Use the product info to answer clearly."
    final_prompt = f"Here are the available products:\n\n{product_text}\n\nUser question: {user_input}"
    if openai.api_key:
        response = openai_answer(system_prompt, final_prompt)
        st.success(response)
    else:
        st.warning("Please enter your OpenAI API key.")

st.markdown("---")

# Button-based mode
st.subheader("🧭 Advisor Tools")
if st.checkbox("Check Client Servicing Opportunities"):
    profile = st.text_area("Enter Client Profile Summary:",
                           "41 years old, Married, 1 daughter, has Singlife Shield Plan 2, Singlife Health Plus")
    summary = st.text_area("Enter Key Portfolio Notes:",
                           "Medishield Life, Singlife Shield Plan, Health Plus only")
    if st.button("Analyze Gaps"):
        result = analyze_client_gaps(profile, summary)
        st.info("\n".join(result) if result else "No major gaps detected.")

if st.checkbox("Compare Two Products"):
    plan_options = products_df['Plan Name'].tolist()
    plan1 = st.selectbox("Select First Plan", plan_options)
    plan2 = st.selectbox("Select Second Plan", plan_options, index=1)
    if st.button("Compare Plans"):
        question = f"Compare these two plans: {plan1} vs {plan2}"
        compare_prompt = f"Here are the products:\n{product_text}\n\n{question}"
        if openai.api_key:
            result = openai_answer("You are an expert insurance assistant.", compare_prompt)
            st.success(result)
        else:
            st.warning("Please enter your OpenAI API key.")
