import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Comprehensive Financial Dashboard", layout="wide")

# Load the CSV file from GitHub
@st.cache_data
def load_data_from_github():
    file_url = "https://raw.githubusercontent.com/CRF-Software/FinancialReporting-/main/financial_sample_data.csv"
    data = pd.read_csv(file_url)
    data['Date'] = pd.to_datetime(data['Date'])
    return data

# Main Streamlit App
def main():
    # Logo URL
    logo_url = "https://d161ew7sqkx7j0.cloudfront.net/public/images/logos/6698_2300_Childrens_Rescue_Fund_Logo_Final.png"

    # Display logo and center it using HTML
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="{logo_url}" alt="Logo" style="width:300px;">
        </div>
        """,
        unsafe_allow_html=True
    )

    # Page Title
    st.title("Comprehensive Financial Dashboard")

    # Load the financial data from GitHub
    data = load_data_from_github()

    # Sidebar Filters
    st.sidebar.header("Filter Data")
    selected_branch = st.sidebar.multiselect("Select Branch", options=data['Branch_ID'].unique(), default=data['Branch_ID'].unique())
    selected_department = st.sidebar.multiselect("Select Department", options=data['Department'].unique(), default=data['Department'].unique())
    selected_payment_method = st.sidebar.multiselect("Select Payment Method", options=data['Payment_Method'].unique(), default=data['Payment_Method'].unique())
    
    # Date range selection
    date_range = st.sidebar.date_input("Select Date Range", [data['Date'].min().date(), data['Date'].max().date()])
    start_date = datetime.combine(date_range[0], datetime.min.time())
    end_date = datetime.combine(date_range[1], datetime.max.time())

    # Filter data based on sidebar selections
    filtered_data = data[
        (data['Branch_ID'].isin(selected_branch)) &
        (data['Department'].isin(selected_department)) &
        (data['Payment_Method'].isin(selected_payment_method)) &
        (data['Date'].between(start_date, end_date))
    ]

    # Display Key Metrics
    st.subheader("Key Financial Metrics")
    total_credits = filtered_data[filtered_data['Transaction_Type'] == 'Credit']['Transaction_Amount'].sum()
    total_debits = filtered_data[filtered_data['Transaction_Type'] == 'Debit']['Transaction_Amount'].sum()
    total_balance = filtered_data['Balance'].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Credits", f"${total_credits:,.2f}")
    col2.metric("Total Debits", f"${total_debits:,.2f}")
    col3.metric("Total Account Balance", f"${total_balance:,.2f}")

    st.markdown("---")

    ### Additional Comparisons ###

    # Revenue vs Expenses Over Time
    st.subheader("Revenue vs Expenses Over Time")
    revenue_vs_expenses = filtered_data[filtered_data['Transaction_Type'].isin(['Revenue', 'Expense'])]
    revenue_expenses_over_time = revenue_vs_expenses.groupby(['Date', 'Transaction_Type'])['Transaction_Amount'].sum().reset_index()
    fig_revenue_expenses = px.line(revenue_expenses_over_time, x='Date', y='Transaction_Amount', color='Transaction_Type', title="Revenue vs Expenses Over Time")
    st.plotly_chart(fig_revenue_expenses)

    # Gross Profit Margin
    st.subheader("Gross Profit Margin")
    gross_profit_margin = (filtered_data[filtered_data['Transaction_Type'] == 'Revenue']['Transaction_Amount'].sum() - 
                           filtered_data[filtered_data['Transaction_Type'] == 'COGS']['Transaction_Amount'].sum()) / \
                           filtered_data[filtered_data['Transaction_Type'] == 'Revenue']['Transaction_Amount'].sum()
    st.metric("Gross Profit Margin", f"{gross_profit_margin:.2%}")

    # Cash Flow Over Time
    st.subheader("Cash Flow Over Time")
    cash_flow_data = filtered_data[filtered_data['Transaction_Type'].isin(['Revenue', 'Expense'])]
    cash_flow_data['Cash_Flow'] = cash_flow_data.apply(lambda row: row['Transaction_Amount'] if row['Transaction_Type'] == 'Revenue' else -row['Transaction_Amount'], axis=1)
    cash_flow_over_time = cash_flow_data.groupby('Date')['Cash_Flow'].sum().reset_index()
    fig_cash_flow = px.line(cash_flow_over_time, x='Date', y='Cash_Flow', title="Net Cash Flow Over Time")
    st.plotly_chart(fig_cash_flow)

    # Departmental Efficiency (Revenue vs Expenses by Department)
    st.subheader("Departmental Efficiency: Revenue vs Expenses")
    dept_revenue_expenses = filtered_data[filtered_data['Transaction_Type'].isin(['Revenue', 'Expense'])].groupby(['Department', 'Transaction_Type'])['Transaction_Amount'].sum().reset_index()
    fig_dept_efficiency = px.bar(dept_revenue_expenses, x='Department', y='Transaction_Amount', color='Transaction_Type', title="Departmental Efficiency: Revenue vs Expenses", barmode='group')
    st.plotly_chart(fig_dept_efficiency)

    # Customer Lifetime Value (CLV)
    st.subheader("Customer Lifetime Value")
    customer_lifetime_value = filtered_data.groupby('Customer_ID')['Transaction_Amount'].sum().reset_index().sort_values(by='Transaction_Amount', ascending=False)
    fig_clv = px.bar(customer_lifetime_value.head(10), x='Customer_ID', y='Transaction_Amount', title="Top 10 Customers by Lifetime Value")
    st.plotly_chart(fig_clv)

    # Expense Breakdown by Category
    st.subheader("Expense Breakdown by Category")
    expense_by_category = filtered_data[filtered_data['Transaction_Type'] == 'Expense'].groupby('Department')['Transaction_Amount'].sum().reset_index()
    fig_expense_category = px.pie(expense_by_category, values='Transaction_Amount', names='Department', title="Expense Breakdown by Category")
    st.plotly_chart(fig_expense_category)

    # Accounts Receivable and Payable
    st.subheader("Accounts Receivable vs Payable")
    receivables = filtered_data[filtered_data['Transaction_Type'] == 'Receivable']['Transaction_Amount'].sum()
    payables = filtered_data[filtered_data['Transaction_Type'] == 'Payable']['Transaction_Amount'].sum()
    col1, col2 = st.columns(2)
    col1.metric("Total Receivables", f"${receivables:,.2f}")
    col2.metric("Total Payables", f"${payables:,.2f}")

    # Operating Cash Flow
    st.subheader("Operating Cash Flow")
    operating_cash_flow = filtered_data[filtered_data['Transaction_Type'] == 'Revenue']['Transaction_Amount'].sum() - filtered_data[filtered_data['Transaction_Type'] == 'Expense']['Transaction_Amount'].sum()
    st.metric("Operating Cash Flow", f"${operating_cash_flow:,.2f}")

    # Debt-to-Equity Ratio
    st.subheader("Debt-to-Equity Ratio")
    total_debt = filtered_data[filtered_data['Transaction_Type'] == 'Debt']['Transaction_Amount'].sum()
    total_equity = filtered_data[filtered_data['Transaction_Type'] == 'Equity']['Transaction_Amount'].sum()
    debt_to_equity_ratio = (total_debt / total_equity) if total_equity > 0 else 0
    st.metric("Debt-to-Equity Ratio", f"{debt_to_equity_ratio:.2f}")

    # Net Profit Margin
    st.subheader("Net Profit Margin")
    net_profit_margin = (total_credits - total_debits) / total_credits if total_credits > 0 else 0
    st.metric("Net Profit Margin", f"{net_profit_margin:.2%}")

    # Return on Assets (ROA)
    st.subheader("Return on Assets (ROA)")
    total_assets = filtered_data['Balance'].sum()  # Assuming 'Balance' represents total assets
    roa = (total_credits - total_debits) / total_assets if total_assets > 0 else 0
    st.metric("Return on Assets", f"{roa:.2%}")

    st.markdown("---")
    
    # Footer note
    st.markdown("""
    ---
    **Note:** This dashboard provides real-time insights into financial transactions, 
    balances, customer trends, tax, discounts, and more for financial teams and CFOs.
    """)

if __name__ == "__main__":
    main()
