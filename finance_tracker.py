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

if 'delete_id' not in st.session_state:
    st.session_state.delete_id = None

if 'refresh' not in st.session_state:
    st.session_state.refresh = False

def set_delete_id(id):
    st.session_state.delete_id = id

def delete_transaction():
    if st.session_state.delete_id is not None:
        st.session_state.transactions = st.session_state.transactions.drop(st.session_state.delete_id)
        save_transactions(st.session_state.transactions)
        st.session_state.delete_id = None
        st.session_state.refresh = True

def cancel_delete():
    st.session_state.delete_id = None

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
            st.session_state.refresh = True

    # Main area for displaying data and charts
    if st.session_state.refresh:
        st.session_state.transactions = load_transactions()
        st.session_state.refresh = False

    if not st.session_state.transactions.empty:
        st.header("Financial Overview")
        
        # Display transactions with a delete button for each
        st.subheader("Transactions")
        for index, row in st.session_state.transactions.iterrows():
            col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 3, 1.5])
            col1.write(row['Date'].strftime('%Y-%m-%d'))
            col2.write(f"${row['Amount']:.2f}")
            col3.write(row['Category'])
            col4.write(row['Type'])
            col5.write(row['Details'])
            col6.button('Delete', key=f"del_{index}", on_click=set_delete_id, args=(index,), use_container_width=True)

        # Pop-up confirmation
        if st.session_state.delete_id is not None:
            with st.expander("Confirm Deletion", expanded=True):
                st.write("Are you sure you want to delete this transaction?")
                col1, col2 = st.columns(2)
                col1.button("Yes, Delete", on_click=delete_transaction)
                col2.button("Cancel", on_click=cancel_delete)

        # Calculate total revenue and expenses
        total_revenue = st.session_state.transactions[st.session_state.transactions['Type'] == 'Revenue']['Amount'].sum()
        total_expenses = st.session_state.transactions[st.session_state.transactions['Type'] == 'Expense']['Amount'].sum()
        net_income = total_revenue - total_expenses

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Revenue", f"${total_revenue:.2f}")
        col2.metric("Total Expenses", f"${total_expenses:.2f}")
        col3.metric("Net Income", f"${net_income:.2f}")

        # Expenses by category pie chart
        expenses_by_category = st.session_state.transactions[st.session_state.transactions['Type'] == 'Expense']
        fig_expense_category = px.pie(expenses_by_category, values='Amount', names='Category', title='Expenses by Category')
        st.plotly_chart(fig_expense_category)

        # Revenue by category pie chart
        revenue_by_category = st.session_state.transactions[st.session_state.transactions['Type'] == 'Revenue']
        fig_revenue_category = px.pie(revenue_by_category, values='Amount', names='Category', title='Revenue by Category')
        st.plotly_chart(fig_revenue_category)

        # Transactions over time line chart
        fig_time = px.line(st.session_state.transactions, x='Date', y='Amount', color='Type', 
                           title='Transactions Over Time')
        st.plotly_chart(fig_time)

    else:
        st.info("No transactions recorded yet. Add some transactions to see your financial overview!")

if __name__ == "__main__":
    main()