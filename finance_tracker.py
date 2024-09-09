import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# File to store transactions
TRANSACTIONS_FILE = "transactions.csv"

# Load transactions from file
def load_transactions():
    if os.path.exists(TRANSACTIONS_FILE):
        return pd.read_csv(TRANSACTIONS_FILE, parse_dates=['Date'])
    return pd.DataFrame(columns=['Date', 'Amount', 'Category', 'Type', 'Details'])

# Save transactions to file
def save_transactions(transactions):
    transactions.to_csv(TRANSACTIONS_FILE, index=False)

# Initialize session state
if 'transactions' not in st.session_state:
    st.session_state.transactions = load_transactions()

def main():
    st.title("Personal Finance Tracker")

    # Sidebar for adding new transactions
    with st.sidebar:
        st.header("Add New Transaction")
        date = st.date_input("Date", datetime.now())
        amount = st.number_input("Amount", min_value=0.00, value=0.00, step=1.00)
        category = st.selectbox("Category", ["Salary", "Investments", "Food", "Transportation", "Entertainment", "Utilities", "Other"])
        transaction_type = st.radio("Type", ["Revenue", "Expense"])
        details = st.text_input("Details", "")
        
        if st.button("Add Transaction"):
            new_transaction = pd.DataFrame([[date, amount, category, transaction_type, details]], 
                                           columns=['Date', 'Amount', 'Category', 'Type', 'Details'])
            st.session_state.transactions = pd.concat([st.session_state.transactions, new_transaction], ignore_index=True)
            save_transactions(st.session_state.transactions)
            st.success("Transaction added successfully!")

    # Main area for displaying data and charts
    transactions = load_transactions()  # Load transactions every time the app refreshes
    if not transactions.empty:
        st.header("Financial Overview")
        st.dataframe(transactions)

        # Calculate total revenue and expenses
        total_revenue = transactions[transactions['Type'] == 'Revenue']['Amount'].sum()
        total_expenses = transactions[transactions['Type'] == 'Expense']['Amount'].sum()
        net_income = total_revenue - total_expenses

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Revenue", f"${total_revenue:.2f}")
        col2.metric("Total Expenses", f"${total_expenses:.2f}")
        col3.metric("Net Income", f"${net_income:.2f}")

        # Expenses by category pie chart
        expenses_by_category = transactions[transactions['Type'] == 'Expense']
        fig_expense_category = px.pie(expenses_by_category, values='Amount', names='Category', title='Expenses by Category')
        st.plotly_chart(fig_expense_category)

        # Revenue by category pie chart
        revenue_by_category = transactions[transactions['Type'] == 'Revenue']
        fig_revenue_category = px.pie(revenue_by_category, values='Amount', names='Category', title='Revenue by Category')
        st.plotly_chart(fig_revenue_category)

        # Transactions over time line chart
        fig_time = px.line(transactions, x='Date', y='Amount', color='Type', 
                           title='Transactions Over Time')
        st.plotly_chart(fig_time)

    else:
        st.info("No transactions recorded yet. Add some transactions to see your financial overview!")

if __name__ == "__main__":
    main()