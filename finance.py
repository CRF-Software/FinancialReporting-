import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Non-Profit CFO Comparative Dashboard", layout="wide")

# Load data from Excel file
@st.cache_data
def load_data():
    file_path = "non_profit_financial_data.xlsx"  # Adjust if needed
    shelter_operations = pd.read_excel(file_path, sheet_name="Shelter Operations")
    funding_sources = pd.read_excel(file_path, sheet_name="Funding Sources")
    donors = pd.read_excel(file_path, sheet_name="Donor Contributions")
    payroll = pd.read_excel(file_path, sheet_name="Payroll Data")
    grant_allocations = pd.read_excel(file_path, sheet_name="Grant Allocations")
    utilities = pd.read_excel(file_path, sheet_name="Utilities Data")
    
    shelter_operations['Date'] = pd.to_datetime(shelter_operations['Date'])
    
    return shelter_operations, funding_sources, donors, payroll, grant_allocations, utilities

# Main dashboard app
def main():
    st.title("Comparative CFO Dashboard - Non-Profit Organization")

    # Load the data
    shelter_operations, funding_sources, donors, payroll, grant_allocations, utilities = load_data()

    # Sidebar filters
    st.sidebar.header("Filter Data")
    selected_shelter = st.sidebar.multiselect("Select Shelter Location", shelter_operations['Shelter_Location'].unique(), default=shelter_operations['Shelter_Location'].unique())
    selected_date_range = st.sidebar.date_input("Select Date Range", [shelter_operations['Date'].min(), shelter_operations['Date'].max()])

    # Filter based on sidebar selections
    start_date, end_date = selected_date_range
    filtered_data = shelter_operations[(shelter_operations['Shelter_Location'].isin(selected_shelter)) & 
                                       (shelter_operations['Date'] >= pd.to_datetime(start_date)) & 
                                       (shelter_operations['Date'] <= pd.to_datetime(end_date))]

    # Display key financial metrics
    st.subheader("Key Financial Metrics")
    
    total_daily_cost = filtered_data['Total_Daily_Cost'].sum()
    avg_occupancy = filtered_data['Occupancy_Rate (%)'].mean()
    total_funding_received = funding_sources['Funding_Amount'].sum()
    total_donations = donors['Donation_Amount'].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Daily Cost", f"${total_daily_cost:,.2f}")
    col2.metric("Average Occupancy Rate", f"{avg_occupancy:.2f}%")
    col3.metric("Total Funding Received", f"${total_funding_received:,.2f}")
    col4.metric("Total Donations", f"${total_donations:,.2f}")

    st.markdown("---")

    # Compare Shelters by Daily Operating Costs
    st.subheader("Compare Daily Operating Costs by Shelter")
    selected_compare_shelters = st.multiselect("Select Shelters to Compare", shelter_operations['Shelter_Location'].unique(), default=shelter_operations['Shelter_Location'].unique())
    
    compare_shelter_data = shelter_operations[(shelter_operations['Shelter_Location'].isin(selected_compare_shelters)) & 
                                              (shelter_operations['Date'] >= pd.to_datetime(start_date)) & 
                                              (shelter_operations['Date'] <= pd.to_datetime(end_date))]
    
    costs_comparison = compare_shelter_data.groupby(['Date', 'Shelter_Location'])['Total_Daily_Cost'].sum().reset_index()
    fig_costs_comparison = px.line(costs_comparison, x='Date', y='Total_Daily_Cost', color='Shelter_Location', title="Comparative Daily Costs Across Shelters")
    st.plotly_chart(fig_costs_comparison, use_container_width=True)

    # Compare Occupancy Rates by Shelter
    st.subheader("Compare Occupancy Rates by Shelter")
    compare_occupancy = compare_shelter_data.groupby(['Date', 'Shelter_Location'])['Occupancy_Rate (%)'].mean().reset_index()
    fig_occupancy_comparison = px.line(compare_occupancy, x='Date', y='Occupancy_Rate (%)', color='Shelter_Location', title="Comparative Occupancy Rates Across Shelters")
    st.plotly_chart(fig_occupancy_comparison, use_container_width=True)

    # Comparative Funding Sources by Source Type
    st.subheader("Compare Funding Sources")
    selected_funding_type = st.selectbox("Select Funding Type", funding_sources['Funding_Type'].unique())
    funding_filtered = funding_sources[funding_sources['Funding_Type'] == selected_funding_type]

    fig_funding_comparison = px.pie(funding_filtered, values='Funding_Amount', names='Source_Name', title=f"Funding Breakdown - {selected_funding_type}")
    st.plotly_chart(fig_funding_comparison, use_container_width=True)

    # Comparative Donor Contributions
    st.subheader("Compare Donor Contributions by Donor Type")
    selected_donor_type = st.multiselect("Select Donor Type", donors['Donor_Type'].unique(), default=donors['Donor_Type'].unique())
    donor_filtered = donors[donors['Donor_Type'].isin(selected_donor_type)]

    fig_donor_comparison = px.bar(donor_filtered, x='Donor_Name', y='Donation_Amount', color='Donor_Type', title="Comparative Donor Contributions")
    st.plotly_chart(fig_donor_comparison, use_container_width=True)

    # Payroll Comparison by Role
    st.subheader("Compare Payroll by Role")
    selected_roles = st.multiselect("Select Roles to Compare", payroll['Role'].unique(), default=payroll['Role'].unique())
    payroll_filtered = payroll[payroll['Role'].isin(selected_roles)]

    fig_payroll_comparison = px.bar(payroll_filtered, x='Role', y='Total_Compensation', color='Role', title="Payroll Comparison by Role")
    st.plotly_chart(fig_payroll_comparison, use_container_width=True)

    # Compare Utilities Costs
    st.subheader("Compare Utilities Costs by Type")
    selected_utility_type = st.multiselect("Select Utility Type", utilities['Utility_Type'].unique(), default=utilities['Utility_Type'].unique())
    utilities_filtered = utilities[utilities['Utility_Type'].isin(selected_utility_type)]

    fig_utilities_comparison = px.bar(utilities_filtered, x='Utility_Type', y='Utility_Cost', color='Utility_Type', title="Comparative Utilities Costs by Type")
    st.plotly_chart(fig_utilities_comparison, use_container_width=True)

    st.markdown("---")

    # Footer
    st.markdown("""
    ---
    **Note:** This dashboard provides a comparative overview of financial operations for shelters, 
    including comparisons across shelters, funding sources, donors, payroll, and utilities costs.
    """)

if __name__ == "__main__":
    main()
