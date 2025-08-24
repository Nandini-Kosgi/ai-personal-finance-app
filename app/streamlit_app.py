import os
import io
from datetime import datetime
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from modules.simulators import butterfly_effect, scenario_tester
from modules.llm_bot import chat

load_dotenv()

st.set_page_config(page_title="AI Assisted Personal Finance", layout="wide")

# ---------------- Auth (simple demo) ----------------
USR = os.getenv("APP_USERNAME")
PWD = os.getenv("APP_PASSWORD")
if USR and PWD:
    with st.sidebar:
        st.markdown("### Login")
        u = st.text_input("Username", value="", key="u")
        p = st.text_input("Password", type="password", value="", key="p")
        if not (u == USR and p == PWD):
            st.stop()

# ---------------- Sidebar nav ----------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Getting Started", "Upload Data", "Overview",
                                  "Income/Expense", "Financial Foresight", "Custom Bot"])

if "df" not in st.session_state:
    # Load bundled sample if present
    sample_path = os.path.join(os.path.dirname(__file__), "..", "data", "transactions_large.csv")
    if os.path.exists(sample_path):
        st.session_state.df = pd.read_csv(sample_path, parse_dates=["date"])
    else:
        st.session_state.df = pd.DataFrame()

def load_overview(df: pd.DataFrame):
    st.header("Monthly Income & Expenses")
    if df.empty:
        st.info("Upload data to see charts.")
        return
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    g = df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0.0)
    g = g.rename(columns={"income": "Income", "expense": "Expenses"})
    st.line_chart(g)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Recent activity")
        recent = df.sort_values("date", ascending=False).head(5)
        for _, r in recent.iterrows():
            color = "red" if r["type"] == "expense" else "green"
            st.markdown(f"**{r['date'].date()}** — {r['category']} — "
                        f"<span style='color:{color}'>${r['amount']:.2f}</span>", unsafe_allow_html=True)
    with c2:
        st.subheader("Spending categories")
        exp = df[df["type"]=="expense"]
        pie = exp.groupby("category")["amount"].sum().sort_values(ascending=False).head(8)
        fig, ax = plt.subplots()
        ax.pie(pie.values, labels=pie.index, autopct='%1.0f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

def page_getting_started():
    st.title("AI Assisted Personal Finance Management System")
    st.markdown("""A privacy-first financial management tool demonstrating the compounding effects of small financial changes and enabling stress testing of financial scenarios.
""")
    st.markdown("### Features")
    st.markdown("- **Butterfly Effect Simulator** — see long-term effects of small changes.")
    st.markdown("- **Financial Scenario Tester** — stress test market/job/medical shocks.")
    st.markdown("- **AI-Powered Assistant** — chat about your finances (optional).")

def page_upload():
    st.title("Upload Data")
    st.write("Upload a CSV with columns: `date, description, category, amount, type`")
    f = st.file_uploader("transactions.csv", type=["csv"])
    if f:
        df = pd.read_csv(f, parse_dates=["date"])
        st.session_state.df = df
        st.success("Loaded! Go to Overview.")
        st.dataframe(df.head(10))

def page_overview():
    st.title("Overview")
    load_overview(st.session_state.df)

def page_income_expense():
    st.title("Income / Expense Explorer")
    df = st.session_state.df
    if df.empty:
        st.info("Upload data first.")
        return
    m = df.copy()
    m["month"] = m["date"].dt.to_period("M").dt.to_timestamp()
    sel_cat = st.multiselect("Categories", options=sorted(m["category"].unique()))
    if sel_cat:
        m = m[m["category"].isin(sel_cat)]
    st.bar_chart(m.groupby(["month","type"])["amount"].sum().unstack(fill_value=0.0))

def page_financial_foresight():
    st.title("Financial Foresight")
    st.subheader("Butterfly Effect Simulator")
    c1, c2 = st.columns(2)
    with c1:
        start_balance = st.number_input("Starting balance ($)", 0.0, 1e7, 5000.0, step=100.0)
        monthly_contrib = st.number_input("Monthly contribution ($)", 0.0, 1e6, 400.0, step=10.0)
        delta_pct = st.number_input("Increase contribution by (%)", -100.0, 500.0, 10.0, step=1.0)
        years = st.slider("Years", 1, 40, 10)
    with c2:
        annual_return = st.slider("Annual return (mean)", 0.0, 0.20, 0.06, 0.01)
        annual_vol = st.slider("Annual volatility", 0.0, 0.40, 0.10, 0.01)
        seed = st.number_input("Random seed", 0, 1_000_000, 42, step=1)

    if st.button("Run Butterfly Effect"):
        df = butterfly_effect(start_balance, monthly_contrib, delta_pct, years, annual_return, annual_vol, seed)
        st.line_chart(df.set_index("month")[["baseline","adjusted"]])
        st.metric("Delta after {} years".format(years), f"${df['delta'].iloc[-1]:.0f}")

    st.divider()
    st.subheader("Financial Scenario Tester (Monte Carlo)")
    c1, c2 = st.columns(2)
    with c1:
        inc = st.number_input("Monthly income ($)", 0.0, 1e6, 5000.0, step=50.0)
        exp = st.number_input("Monthly expense ($)", 0.0, 1e6, 3500.0, step=50.0)
        target = st.number_input("Emergency fund target ($)", 0.0, 1e7, 10000.0, step=100.0)
        horizon = st.slider("Horizon (months)", 6, 120, 36)
    with c2:
        job = st.slider("Job-loss prob / month", 0.0, 0.20, 0.01, 0.001)
        medp = st.slider("Medical bill prob / month", 0.0, 0.20, 0.02, 0.001)
        meda = st.number_input("Medical bill amount ($)", 0.0, 1e6, 1500.0, step=50.0)
        sims = st.slider("Simulations", 100, 10000, 2000, 100)

    if st.button("Run Scenario Test"):
        out = scenario_tester(inc, exp, target, horizon, job, medp, meda, sims=sims)
        st.metric("Success probability", f"{out['success_rate']*100:.1f}%")
        col = st.columns(4)
        col[0].metric("P10", f"${out['p10']:.0f}")
        col[1].metric("P50", f"${out['p50']:.0f}")
        col[2].metric("P90", f"${out['p90']:.0f}")
        col[3].metric("Mean", f"${out['mean_end_balance']:.0f}")

def page_custom_bot():
    st.title("AI-Powered Assistant")
    st.caption("Reminder: Informational only — not financial advice.")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    user_msg = st.text_input("Ask a question about your budget/transactions:")
    if st.button("Send") and user_msg.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        reply = chat(st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
    for turn in st.session_state.chat_history[-8:]:
        st.markdown(f"**{turn['role'].capitalize()}:** {turn['content']}")

# ---------------- Route pages ----------------
if page == "Getting Started":
    page_getting_started()
elif page == "Upload Data":
    page_upload()
elif page == "Overview":
    page_overview()
elif page == "Income/Expense":
    page_income_expense()
elif page == "Financial Foresight":
    page_financial_foresight()
else:
    page_custom_bot()
