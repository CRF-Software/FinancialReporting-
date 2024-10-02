
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Comprehensive Financial Dashboard", layout="wide")

# Load the CSV file from GitHub
@st.cache_data
def load_data_from_github(file_url):
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
    file_url = "https://raw.githubusercontent.com/CRF-Software/FinancialReporting-/main/financial_sample_data.csv"
    data = load_data_from_github(file_url)

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

    ### Transaction Comparisons ###

    # Smaller plot dimensions for better layout
    plot_height = 350
    plot_width = 600

    # Transaction Amount by Type
    st.subheader("Transaction Amount by Type")
    transaction_by_type = filtered_data.groupby('Transaction_Type')['Transaction_Amount'].sum().reset_index()
    fig1 = px.bar(transaction_by_type, x='Transaction_Type', y='Transaction_Amount', title="Transaction Amount by Type", width=plot_width, height=plot_height)
    st.plotly_chart(fig1, use_container_width=False)

    # Transaction Volume by Payment Method
    st.subheader("Transaction Volume by Payment Method")
    transaction_by_payment_method = filtered_data.groupby('Payment_Method')['Transaction_Amount'].sum().reset_index()
    fig2 = px.pie(transaction_by_payment_method, values='Transaction_Amount', names='Payment_Method', title="Transaction Volume by Payment Method", width=plot_width, height=plot_height)
    st.plotly_chart(fig2, use_container_width=False)

    # Transaction Amount by Department
    st.subheader("Transaction Amount by Department")
    transaction_by_department = filtered_data.groupby('Department')['Transaction_Amount'].sum().reset_index()
    fig3 = px.bar(transaction_by_department, x='Department', y='Transaction_Amount', title="Transaction Amount by Department", width=plot_width, height=plot_height)
    st.plotly_chart(fig3, use_container_width=False)

    ### Balance Analysis ###

    # Balance by Branch
    st.subheader("Balance by Branch")
    balance_by_branch = filtered_data.groupby('Branch_ID')['Balance'].sum().reset_index()
    fig4 = px.bar(balance_by_branch, x='Branch_ID', y='Balance', title="Balance by Branch", width=plot_width, height=plot_height)
    st.plotly_chart(fig4, use_container_width=False)

    # Balance by Payment Method
    st.subheader("Balance by Payment Method")
    balance_by_payment_method = filtered_data.groupby('Payment_Method')['Balance'].sum().reset_index()
    fig5 = px.bar(balance_by_payment_method, x='Payment_Method', y='Balance', title="Balance by Payment Method", width=plot_width, height=plot_height)
    st.plotly_chart(fig5, use_container_width=False)

    ### Customer Analysis ###

    # Top 10 Customers by Transaction Amount
    st.subheader("👥 Top 10 Customers by Transaction Amount")
    top_customers = filtered_data.groupby('Customer_ID')['Transaction_Amount'].sum().nlargest(10).reset_index()
    fig6 = px.bar(top_customers, x='Customer_ID', y='Transaction_Amount', title="Top 10 Customers by Transaction Amount", width=plot_width, height=plot_height)
    st.plotly_chart(fig6, use_container_width=False)

    ### Tax and Discount Analysis ###

    # Total Tax Amount Over Time
    st.subheader("Total Tax Amount Over Time")
    tax_over_time = filtered_data.groupby('Date')['Tax_Amount'].sum().reset_index()
    fig7 = px.line(tax_over_time, x='Date', y='Tax_Amount', title="Total Tax Amount Over Time", width=plot_width, height=plot_height)
    st.plotly_chart(fig7, use_container_width=False)

    # Total Discounts by Payment Method
    st.subheader("Total Discounts by Payment Method")
    discount_by_payment_method = filtered_data.groupby('Payment_Method')['Discount_Amount'].sum().reset_index()
    fig8 = px.bar(discount_by_payment_method, x='Payment_Method', y='Discount_Amount', title="Discounts by Payment Method", width=plot_width, height=plot_height)
    st.plotly_chart(fig8, use_container_width=False)

    ### Correlation Matrix ###

    st.subheader("Correlation Matrix")
    numeric_data = filtered_data.select_dtypes(include=['float64', 'int64'])
    correlation_matrix = numeric_data.corr()
    fig_corr = px.imshow(correlation_matrix, text_auto=True, title="Correlation Matrix Heatmap", width=plot_width, height=plot_height)
    st.plotly_chart(fig_corr, use_container_width=False)

    st.markdown("---")

# Existing code goes here (if you have any pre-defined functions or imports)

# Load your dataset from GitHub URL
def load_data():
    url = 'https://raw.githubusercontent.com/CRF-Software/FinancialReporting-/main/financial_sample_data.csv'
    return pd.read_csv(url)

# 1. Revenue vs. Expenses Comparison
def calculate_revenue_vs_expenses(data):
    revenue = data[data['Transaction_Type'] == 'Revenue']['Transaction_Amount'].sum()
    expenses = data[data['Transaction_Type'] == 'Expense']['Transaction_Amount'].sum()
    return revenue, expenses

# 2. Gross Profit Margin Calculation
def calculate_gross_profit_margin(data):
    revenue = data[data['Transaction_Type'] == 'Revenue']['Transaction_Amount'].sum()
    cogs = data[data['Transaction_Type'] == 'COGS']['Transaction_Amount'].sum()
    gross_profit = revenue - cogs
    gross_profit_margin = (gross_profit / revenue) * 100 if revenue > 0 else 0
    return gross_profit_margin

# 3. Operating Expenses Calculation
def calculate_operating_expenses(data):
    operating_expenses = data[data['Transaction_Type'] == 'Operating Expense']['Transaction_Amount'].sum()
    return operating_expenses

# 4. Cash Flow Analysis
def calculate_cash_flow(data):
    cash_inflows = data[data['Transaction_Type'].isin(['Revenue', 'Other Income'])]['Transaction_Amount'].sum()
    cash_outflows = data[data['Transaction_Type'].isin(['Expense', 'COGS'])]['Transaction_Amount'].sum()
    return cash_inflows, cash_outflows

# 5. Profitability Ratios (ROA and ROE)
def calculate_profitability_ratios(data, total_assets, total_equity):
    net_income = data[data['Transaction_Type'] == 'Net Income']['Transaction_Amount'].sum()
    roa = (net_income / total_assets) * 100 if total_assets > 0 else 0
    roe = (net_income / total_equity) * 100 if total_equity > 0 else 0
    return roa, roe

# 6. Debt to Equity Ratio Calculation
def calculate_debt_to_equity(total_debt, total_equity):
    debt_to_equity_ratio = (total_debt / total_equity) * 100 if total_equity > 0 else 0
    return debt_to_equity_ratio

# 7. Budget vs. Actual Performance
def calculate_budget_vs_actual(data, budgeted_revenue, budgeted_expenses):
    actual_revenue = data[data['Transaction_Type'] == 'Revenue']['Transaction_Amount'].sum()
    actual_expenses = data[data['Transaction_Type'] == 'Expense']['Transaction_Amount'].sum()
    revenue_diff = actual_revenue - budgeted_revenue
    expense_diff = actual_expenses - budgeted_expenses
    return revenue_diff, expense_diff

# Main function to run all calculations
def run_financial_analysis(total_assets, total_equity, total_debt, budgeted_revenue, budgeted_expenses):
    data = load_data()

    # Calculate comparisons
    revenue, expenses = calculate_revenue_vs_expenses(data)
    gross_profit_margin = calculate_gross_profit_margin(data)
    operating_expenses = calculate_operating_expenses(data)
    cash_inflows, cash_outflows = calculate_cash_flow(data)
    roa, roe = calculate_profitability_ratios(data, total_assets, total_equity)
    debt_to_equity_ratio = calculate_debt_to_equity(total_debt, total_equity)
    revenue_diff, expense_diff = calculate_budget_vs_actual(data, budgeted_revenue, budgeted_expenses)

    # Print out the results
    print(f"Revenue: ${revenue}")
    print(f"Expenses: ${expenses}")
    print(f"Gross Profit Margin: {gross_profit_margin}%")
    print(f"Operating Expenses: ${operating_expenses}")
    print(f"Cash Inflows: ${cash_inflows}, Cash Outflows: ${cash_outflows}")
    print(f"Return on Assets (ROA): {roa}%, Return on Equity (ROE): {roe}%")
    print(f"Debt to Equity Ratio: {debt_to_equity_ratio}%")
    print(f"Budget vs Actual Revenue Difference: ${revenue_diff}")
    print(f"Budget vs Actual Expense Difference: ${expense_diff}")

# Example usage with real data
total_assets = 500000  # Replace with actual total assets
total_equity = 300000  # Replace with actual total equity
total_debt = 200000  # Replace with actual total debt
budgeted_revenue = 100000  # Replace with budgeted revenue
budgeted_expenses = 80000  # Replace with budgeted expenses

run_financial_analysis(total_assets, total_equity, total_debt, budgeted_revenue, budgeted_expenses)

    # Footer note
    st.markdown("""
    ---
    **Note:** This dashboard provides real-time insights into financial transactions, 
    balances, customer trends, tax, discounts, and more for financial teams and CFOs.
    """)

if __name__ == "__main__":
    main()
