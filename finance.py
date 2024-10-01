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
    # Page Title
    st.title("📊 Comprehensive Financial Dashboard")

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
    st.subheader("💰 Key Financial Metrics")
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
    st.subheader("🔄 Transaction Amount by Type")
    transaction_by_type = filtered_data.groupby('Transaction_Type')['Transaction_Amount'].sum().reset_index()
    fig1 = px.bar(transaction_by_type, x='Transaction_Type', y='Transaction_Amount', title="Transaction Amount by Type", width=plot_width, height=plot_height)
    st.plotly_chart(fig1, use_container_width=False)

    # Transaction Volume by Payment Method
    st.subheader("💳 Transaction Volume by Payment Method")
    transaction_by_payment_method = filtered_data.groupby('Payment_Method')['Transaction_Amount'].sum().reset_index()
    fig2 = px.pie(transaction_by_payment_method, values='Transaction_Amount', names='Payment_Method', title="Transaction Volume by Payment Method", width=plot_width, height=plot_height)
    st.plotly_chart(fig2, use_container_width=False)

    # Transaction Amount by Department
    st.subheader("🏢 Transaction Amount by Department")
    transaction_by_department = filtered_data.groupby('Department')['Transaction_Amount'].sum().reset_index()
    fig3 = px.bar(transaction_by_department, x='Department', y='Transaction_Amount', title="Transaction Amount by Department", width=plot_width, height=plot_height)
    st.plotly_chart(fig3, use_container_width=False)

    ### Balance Analysis ###

    # Balance by Branch
    st.subheader("🏦 Balance by Branch")
    balance_by_branch = filtered_data.groupby('Branch_ID')['Balance'].sum().reset_index()
    fig4 = px.bar(balance_by_branch, x='Branch_ID', y='Balance', title="Balance by Branch", width=plot_width, height=plot_height)
    st.plotly_chart(fig4, use_container_width=False)

    # Balance by Payment Method
    st.subheader("💳 Balance by Payment Method")
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
    st.subheader("🧾 Total Tax Amount Over Time")
    tax_over_time = filtered_data.groupby('Date')['Tax_Amount'].sum().reset_index()
    fig7 = px.line(tax_over_time, x='Date', y='Tax_Amount', title="Total Tax Amount Over Time", width=plot_width, height=plot_height)
    st.plotly_chart(fig7, use_container_width=False)

    # Total Discounts by Payment Method
    st.subheader("💲 Total Discounts by Payment Method")
    discount_by_payment_method = filtered_data.groupby('Payment_Method')['Discount_Amount'].sum().reset_index()
    fig8 = px.bar(discount_by_payment_method, x='Payment_Method', y='Discount_Amount', title="Discounts by Payment Method", width=plot_width, height=plot_height)
    st.plotly_chart(fig8, use_container_width=False)

    ### Correlation Matrix ###

    st.subheader("📊 Correlation Matrix")
    numeric_data = filtered_data.select_dtypes(include=['float64', 'int64'])
    correlation_matrix = numeric_data.corr()
    fig_corr = px.imshow(correlation_matrix, text_auto=True, title="Correlation Matrix Heatmap", width=plot_width, height=plot_height)
    st.plotly_chart(fig_corr, use_container_width=False)

    st.markdown("---")
    
    # Footer note
    st.markdown("""
    ---
    **Note:** This dashboard provides real-time insights into financial transactions, 
    balances, customer trends, tax, discounts, and more for financial teams and CFOs.
    """)

if __name__ == "__main__":
    main()
