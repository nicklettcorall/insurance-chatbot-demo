# --- app.py ---

import streamlit as st
from utils import load_products, load_clients, openai_answer, analyze_client_gaps

st.set_page_config(page_title="i-NITIATE© Ray Demo", layout="centered")

st.title("i-NITIATE© Ray Demo")
user_api_key = st.text_input("Enter your OpenAI API Key", type="password")

products_df = load_products()
clients_df = load_clients()
product_text = products_df.to_string(index=False)

st.subheader("Chat with Ray")
user_input = st.text_input("Ask a client related question...")
if st.button("Send") and user_input:
    system_prompt = (
        "You are Ray, an AI assistant helping insurance advisors. When asked, analyse the client profile, "
        "identify servicing opportunities, recommend suitable plans, or compare product features based on the provided data. "
        "Always justify your advice using relevant plan information. "
        "Use conversational Tone, make it easier to read by change sentence structures, and break down Big Ideas."
    )
    
    client_text = clients_df.to_string(index=False)
    final_prompt = (
        f"Here are the available products:\n\n{product_text}\n\n"
        f"Here are the current client profiles:\n\n{client_text}\n\n"
        f"Advisor query: {user_input}"
    )
    if user_api_key:
        response = openai_answer(system_prompt, final_prompt, api_key=user_api_key)
        st.success(response)
    else:
        st.warning("Please enter your OpenAI API key.")

st.markdown("---")

st.subheader("Advisor Tools 🔧")

if st.checkbox("Check Client Servicing Opportunities"):
    selected_client = st.selectbox("Select a Client to Analyze", clients_df["Client Name"].tolist())
    client_row = clients_df[clients_df["Client Name"] == selected_client].iloc[0]
    profile = f"{client_row['Age']} years old, {client_row['Marital Status']}, {client_row['Children']}. {client_row['Dependents']}"
    summary = f"{client_row['Client Plans']}. {client_row['Notes']}"
    st.text_area("Client Profile", value=profile, height=100)
    st.text_area("Portfolio Summary", value=summary, height=100)
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
        if user_api_key:
            result = openai_answer(
                "You are Ray, an AI assistant for insurance advisors. Compare the selected products clearly, highlighting use cases and justifications.",
                compare_prompt,
                api_key=user_api_key
            )
            st.success(result)
        else:
            st.warning("Please enter your OpenAI API key.")
