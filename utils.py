# --- utils.py ---

import pandas as pd
import openai

def load_products(filepath="insurance_products.csv"):
    return pd.read_csv(filepath)

def openai_answer(system_prompt, user_prompt, api_key, model="gpt-3.5-turbo"):
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=800
    )
    return response.choices[0].message.content

def analyze_client_gaps(client_profile, portfolio_summary):
    """ Very simple logic to simulate gap detection """
    gaps = []
    if 'Critical Illness' not in portfolio_summary:
        gaps.append("Missing Critical Illness Protection.")
    if 'Wealth Accumulation' not in portfolio_summary:
        gaps.append("Missing Wealth Accumulation / Education Planning.")
    if 'Retirement Planning' not in portfolio_summary:
        gaps.append("No Retirement Income Plan detected.")
    return gaps
