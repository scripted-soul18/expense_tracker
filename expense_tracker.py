import streamlit as st
import pandas as pd
from datetime import datetime
import os

# CSV file name
CSV_FILE = 'expenses.csv'

# Create the CSV file if it doesn't exist
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Note'])
    df.to_csv(CSV_FILE, index=False)

# Streamlit page settings
st.set_page_config(page_title="💰 Expense Tracker", layout="centered")
st.title("💸 Personal Expense Tracker")

# ------------------- Add New Expense -------------------
st.header("➕ Add New Expense")

with st.form("expense_form"):
    date = st.date_input("Date", datetime.today())
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Others"])
    amount = st.number_input("Amount", min_value=0.0, step=0.5)
    note = st.text_input("Note (optional)")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_data = pd.DataFrame([[date.strftime('%Y-%m-%d'), category, amount, note]],
                                columns=["Date", "Category", "Amount", "Note"])
        new_data.to_csv(CSV_FILE, mode='a', header=False, index=False)
        st.success("✅ Expense added successfully!")

# ------------------- View & Filter Expenses -------------------
st.header("📜 Expense History")
df = pd.read_csv(CSV_FILE)

with st.expander("🔍 Filter Options"):
    category_filter = st.multiselect("Filter by Category", df["Category"].unique())
    if category_filter:
        df = df[df["Category"].isin(category_filter)]

    date_range = st.date_input("Filter by Date Range", [])
    if len(date_range) == 2:
        start, end = [d.strftime('%Y-%m-%d') for d in date_range]
        df = df[(df["Date"] >= start) & (df["Date"] <= end)]

st.dataframe(df)

# ------------------- Summary Charts -------------------
st.header("📊 Expense Summary")
if not df.empty:
    summary = df.groupby("Category")["Amount"].sum()
    st.bar_chart(summary)
else:
    st.info("No expenses to display yet.")
