import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="Accounting & CFO Dashboard", layout="wide")

# Function to load the CSV file from GitHub
def load_data_from_github(file_url):
    data = pd.read_csv(file_url)
    return data

# Main Streamlit App
def main():
    # Page Title
    st.title("📊 Accounting & CFO Dashboard")

    # Load the financial data from GitHub
    file_url = "https://raw.githubusercontent.com/CRF-Software/FinancialReporting-/main/financial_sample_data.csv"
    try:
        data = load_data_from_github(file_url)

        # Format the date column
        data['Date'] = pd.to_datetime(data['Date'])

        # Sidebar Filters for cleaner organization
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

        # Display Key Metrics (cleaner layout with metrics grouped at the top)
        st.subheader("💰 Key Financial Metrics")
        total_credits = filtered_data[filtered_data['Transaction_Type'] == 'Credit']['Transaction_Amount'].sum()
        total_debits = filtered_data[filtered_data['Transaction_Type'] == 'Debit']['Transaction_Amount'].sum()
        total_balance = filtered_data['Balance'].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Credits", f"${total_credits:,.2f}")
        col2.metric("Total Debits", f"${total_debits:,.2f}")
        col3.metric("Total Account Balance", f"${total_balance:,.2f}")

        # Divider for better structure
        st.markdown("---")

        # Transaction Amount Over Time (simplified for better comparison)
        st.subheader("📈 Transaction Amount Over Time")
        fig1 = px.line(filtered_data, x='Date', y='Transaction_Amount', color='Transaction_Type',
                       title="Transaction Amount by Type Over Time", labels={"Transaction_Amount": "Amount (USD)", "Date": "Date"})
        st.plotly_chart(fig1, use_container_width=True)

        # Transaction Breakdown by Branch (side-by-side comparison)
        st.subheader("🏢 Transaction Breakdown by Branch and Department")
        col1, col2 = st.columns(2)

        with col1:
            st.write("**By Branch**")
            fig2 = px.bar(filtered_data, x='Branch_ID', y='Transaction_Amount', color='Transaction_Type', barmode='group',
                          title="Transaction Breakdown by Branch", labels={"Branch_ID": "Branch", "Transaction_Amount": "Amount (USD)"})
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            st.write("**By Department**")
            balance_by_dept = filtered_data.groupby('Department')['Balance'].sum().reset_index()
            fig3 = px.pie(balance_by_dept, values='Balance', names='Department', title="Total Balance by Department")
            st.plotly_chart(fig3, use_container_width=True)

        # Payment Method Distribution
        st.subheader("💳 Payment Method Distribution")
        payment_method_dist = filtered_data['Payment_Method'].value_counts().reset_index()
        fig4 = px.pie(payment_method_dist, values='Payment_Method', names='index', title="Payment Method Distribution", labels={"index": "Payment Method", "Payment_Method": "Count"})
        st.plotly_chart(fig4, use_container_width=True)

        # Tax and Discount Insights (side-by-side comparison for better clarity)
        st.subheader("🧾 Tax and Discount Insights")
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Tax Overview**")
            total_tax = filtered_data['Tax_Amount'].sum()
            fig5 = go.Figure(go.Indicator(
                mode="number+delta",
                value=total_tax,
                title={"text": "Total Tax Amount"},
                delta={"reference": data['Tax_Amount'].sum()},
                number={'prefix': "$"}
            ))
            st.plotly_chart(fig5, use_container_width=True)

        with col2:
            st.write("**Discount Overview**")
            total_discount = filtered_data['Discount_Amount'].sum()
            fig6 = go.Figure(go.Indicator(
                mode="number+delta",
                value=total_discount,
                title={"text": "Total Discount Amount"},
                delta={"reference": data['Discount_Amount'].sum()},
                number={'prefix': "$"}
            ))
            st.plotly_chart(fig6, use_container_width=True)

        # Footer note for clarity and user instruction
        st.markdown("""
        ---
        **Note:** This dashboard provides real-time insights into financial transactions, 
        enabling CFOs and accounting teams to monitor credits, debits, balances, and trends effectively.
        """)
    
    except Exception as e:
        st.error(f"Error loading data: {e}")

if __name__ == "__main__":
    main()
