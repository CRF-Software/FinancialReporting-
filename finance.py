import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Function to load the CSV file from GitHub
def load_data_from_github(file_url):
    data = pd.read_csv(file_url)
    return data

# Main Streamlit App
def main():
    st.set_page_config(page_title="Accounting & CFO Dashboard", layout="wide")
    
    # Page Title
    st.title("Accounting & CFO Dashboard")

    # Load the financial data from GitHub
    file_url = "https://raw.githubusercontent.com/CRF-Software/FinancialReporting-/main/financial_sample_data.csv"
    try:
        data = load_data_from_github(file_url)

        # Format the date column
        data['Date'] = pd.to_datetime(data['Date'])

        # Display Dataset Overview
        st.write("### Dataset Overview")
        st.dataframe(data.head())

        # Display Key Metrics
        total_credits = data[data['Transaction_Type'] == 'Credit']['Transaction_Amount'].sum()
        total_debits = data[data['Transaction_Type'] == 'Debit']['Transaction_Amount'].sum()
        total_balance = data['Balance'].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Credits", f"${total_credits:,.2f}")
        col2.metric("Total Debits", f"${total_debits:,.2f}")
        col3.metric("Total Account Balance", f"${total_balance:,.2f}")

        # Sidebar Filters
        st.sidebar.header("Filter Data")
        selected_branch = st.sidebar.multiselect("Select Branch", options=data['Branch_ID'].unique(), default=data['Branch_ID'].unique())
        selected_department = st.sidebar.multiselect("Select Department", options=data['Department'].unique(), default=data['Department'].unique())
        selected_payment_method = st.sidebar.multiselect("Select Payment Method", options=data['Payment_Method'].unique(), default=data['Payment_Method'].unique())
        date_range = st.sidebar.date_input("Select Date Range", [data['Date'].min(), data['Date'].max()])

        # Filter data based on sidebar selections
        filtered_data = data[
            (data['Branch_ID'].isin(selected_branch)) &
            (data['Department'].isin(selected_department)) &
            (data['Payment_Method'].isin(selected_payment_method)) &
            (data['Date'].between(date_range[0], date_range[1]))
        ]

        st.write(f"### Filtered Data ({len(filtered_data)} records)")
        st.dataframe(filtered_data)

        # Display Visualizations

        # 1. Transaction Amount Over Time
        st.write("### Transaction Amount Over Time")
        fig = px.line(filtered_data, x='Date', y='Transaction_Amount', color='Transaction_Type', title="Transaction Amount by Type Over Time")
        st.plotly_chart(fig, use_container_width=True)

        # 2. Transaction Breakdown by Branch
        st.write("### Transaction Breakdown by Branch")
        fig = px.bar(filtered_data, x='Branch_ID', y='Transaction_Amount', color='Transaction_Type', barmode='group', title="Transaction Breakdown by Branch")
        st.plotly_chart(fig, use_container_width=True)

        # 3. Total Balance by Department
        st.write("### Total Balance by Department")
        balance_by_dept = filtered_data.groupby('Department')['Balance'].sum().reset_index()
        fig = px.pie(balance_by_dept, values='Balance', names='Department', title="Total Balance by Department")
        st.plotly_chart(fig, use_container_width=True)

        # 4. Payment Method Distribution
        st.write("### Payment Method Distribution")
        payment_method_dist = filtered_data['Payment_Method'].value_counts().reset_index()
        fig = px.pie(payment_method_dist, values='Payment_Method', names='index', title="Payment Method Distribution")
        st.plotly_chart(fig, use_container_width=True)

        # 5. Tax and Discount Insights
        st.write("### Tax and Discount Overview")
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=filtered_data['Tax_Amount'].sum(),
            title="Total Tax Amount",
            delta={'reference': data['Tax_Amount'].sum()}
        ))
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=filtered_data['Discount_Amount'].sum(),
            title="Total Discount Amount",
            delta={'reference': data['Discount_Amount'].sum()}
        ))
        st.plotly_chart(fig, use_container_width=True)

        # Footer note
        st.write("This dashboard provides a real-time view of financial data for accounting teams and CFOs, with key insights on transactions, balances, and payment methods.")
    
    except Exception as e:
        st.error(f"Error loading data: {e}")

if __name__ == "__main__":
    main()
