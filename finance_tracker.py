import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Initialize session state
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Amount', 'Category'])

def main():
    st.title("Personal Finance Tracker")

    # Sidebar for adding new expenses
    with st.sidebar:
        st.header("Add New Expense")
        date = st.date_input("Date", datetime.now())
        amount = st.number_input("Amount", min_value=0.00, step=1.00)
        category = st.selectbox("Category", ["Food", "Transportation", "Entertainment", "Utilities", "Other"])
        details = st.text_input("Details")
        if st.button("Add Expense"):
            new_expense = pd.DataFrame([[date, amount, category, details]], columns=['Date', 'Amount', 'Category', 'Details'])
            st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
            st.success("Expense added successfully!")

    # Main area for displaying data and charts
    if not st.session_state.expenses.empty:
        st.header("Expense Overview")
        st.dataframe(st.session_state.expenses)

        # Total expenses
        total_expenses = st.session_state.expenses['Amount'].sum()
        st.metric("Total Expenses", f"${total_expenses:.2f}")

        # Expenses by category pie chart
        fig_category = px.pie(st.session_state.expenses, values='Amount', names='Category', title='Expenses by Category')
        st.plotly_chart(fig_category)

        # Expenses over time line chart
        fig_time = px.line(st.session_state.expenses, x='Date', y='Amount', title='Expenses Over Time')
        st.plotly_chart(fig_time)
    else:
        st.info("No expenses recorded yet. Add some expenses to see your financial overview!")

if __name__ == "__main__":
    main()