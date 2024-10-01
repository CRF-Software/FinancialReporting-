import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="CFO Financial Dashboard", layout="wide")

# Load the CSV file from GitHub
@st.cache_data
def load_data_from_github(file_url):
    data = pd.read_csv(file_url)
    data['Date'] = pd.to_datetime(data['Date'])
    return data

# Main Streamlit App
def main():
    # Logo URL and Title
    logo_url = "https://d161ew7sqkx7j0.cloudfront.net/public/images/logos/6698_2300_Childrens_Rescue_Fund_Logo_Final.png"
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="{logo_url}" alt="Logo" style="width:300px;">
        </div>
        """,
        unsafe_allow_html=True
    )
    st.title("📊 CFO Financial Dashboard")

    # Load financial data from GitHub
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
    st.subheader("💰 Key Financial Metrics")
    total_credits = filtered_data[filtered_data['Transaction_Type'] == 'Credit']['Transaction_Amount'].sum()
    total_debits = filtered_data[filtered_data['Transaction_Type'] == 'Debit']['Transaction_Amount'].sum()
    total_balance = filtered_data['Balance'].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Credits", f"${total_credits:,.2f}")
    col2.metric("Total Debits", f"${total_debits:,.2f}")
    col3.metric("Total Account Balance", f"${total_balance:,.2f}")

    st.markdown("---")

    ### Net Cash Flow Over Time ###
    st.subheader("💸 Net Cash Flow Over Time")
    filtered_data['Net_Cash_Flow'] = filtered_data[filtered_data['Transaction_Type'] == 'Credit']['Transaction_Amount'].sum() - filtered_data[filtered_data['Transaction_Type'] == 'Debit']['Transaction_Amount'].sum()
    net_cash_flow_over_time = filtered_data.groupby('Date')['Net_Cash_Flow'].sum().reset_index()
    fig_cash_flow = px.line(net_cash_flow_over_time, x='Date', y='Net_Cash_Flow', title="Net Cash Flow Over Time")
    st.plotly_chart(fig_cash_flow, use_container_width=True)

    ### Revenue vs. Expenses by Department ###
    st.subheader("💼 Revenue vs. Expenses by Department")
    department_revenue = filtered_data[filtered_data['Transaction_Type'] == 'Credit'].groupby('Department')['Transaction_Amount'].sum().reset_index()
    department_expenses = filtered_data[filtered_data['Transaction_Type'] == 'Debit'].groupby('Department')['Transaction_Amount'].sum().reset_index()
    department_revenue_vs_expenses = pd.merge(department_revenue, department_expenses, on='Department', suffixes=('_Revenue', '_Expenses'))
    fig_revenue_expenses = px.bar(department_revenue_vs_expenses, x='Department', y=['Transaction_Amount_Revenue', 'Transaction_Amount_Expenses'], barmode='group', title="Revenue vs. Expenses by Department")
    st.plotly_chart(fig_revenue_expenses, use_container_width=True)

    ### Revenue to Expense Ratio ###
    st.subheader("📊 Revenue to Expense Ratio by Department")
    department_revenue_vs_expenses['Revenue_to_Expense_Ratio'] = department_revenue_vs_expenses['Transaction_Amount_Revenue'] / department_revenue_vs_expenses['Transaction_Amount_Expenses']
    fig_revenue_ratio = px.bar(department_revenue_vs_expenses, x='Department', y='Revenue_to_Expense_Ratio', title="Revenue to Expense Ratio by Department")
    st.plotly_chart(fig_revenue_ratio, use_container_width=True)

    ### Profitability and Operating Expenses ###
    st.subheader("💼 Profitability and Operating Expenses")
    gross_profit_margin = (total_credits - total_debits) / total_credits * 100
    st.metric("Gross Profit Margin", f"{gross_profit_margin:.2f}%")

    ### Top 10 Customers by Transaction Amount ###
    st.subheader("👥 Top 10 Customers by Transaction Amount")
    top_customers = filtered_data.groupby('Customer_ID')['Transaction_Amount'].sum().nlargest(10).reset_index()
    fig_customers = px.bar(top_customers, x='Customer_ID', y='Transaction_Amount', title="Top 10 Customers by Transaction Amount")
    st.plotly_chart(fig_customers, use_container_width=True)

    ### Customer Profitability ###
    st.subheader("👥 Customer Profitability")
    customer_profitability = filtered_data.groupby('Customer_ID').agg({'Transaction_Amount': 'sum', 'Balance': 'sum'}).reset_index()
    fig_customer_profit = px.scatter(customer_profitability, x='Customer_ID', y='Transaction_Amount', size='Balance', title="Customer Profitability by Transaction Amount and Balance")
    st.plotly_chart(fig_customer_profit, use_container_width=True)

    ### Tax and Discount Analysis ###
    st.subheader("🧾 Tax and Discount Insights")
    total_tax = filtered_data['Tax_Amount'].sum()
    total_discount = filtered_data['Discount_Amount'].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Tax Collected", f"${total_tax:,.2f}")
    col2.metric("Total Discounts Given", f"${total_discount:,.2f}")

    # Total Tax Amount Over Time
    tax_over_time = filtered_data.groupby('Date')['Tax_Amount'].sum().reset_index()
    fig_tax = px.line(tax_over_time, x='Date', y='Tax_Amount', title="Total Tax Amount Over Time")
    st.plotly_chart(fig_tax, use_container_width=True)

    # Total Discounts by Payment Method
    discount_by_payment_method = filtered_data.groupby('Payment_Method')['Discount_Amount'].sum().reset_index()
    fig_discount = px.bar(discount_by_payment_method, x='Payment_Method', y='Discount_Amount', title="Discounts by Payment Method")
    st.plotly_chart(fig_discount, use_container_width=True)

    ### Correlation Matrix ###
    st.subheader("📊 Correlation Matrix")
    numeric_data = filtered_data.select_dtypes(include=['float64', 'int64'])
    correlation_matrix = numeric_data.corr()
    fig_corr = px.imshow(correlation_matrix, text_auto=True, title="Correlation Matrix Heatmap")
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("---")
    
    # Footer note
    st.markdown("""
    ---
    **Note:** This dashboard provides real-time insights into financial transactions, 
    balances, customer trends, tax, discounts, and more for financial teams and CFOs.
    """)

if __name__ == "__main__":
    main()
