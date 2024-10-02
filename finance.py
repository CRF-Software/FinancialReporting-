import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Non-Profit CFO Dashboard", layout="wide")

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
    st.title("CFO Dashboard - Non-Profit Organization")

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

    # Plot: Daily Operating Costs Over Time
    st.subheader("Daily Operating Costs Over Time")
    costs_over_time = filtered_data.groupby('Date')['Total_Daily_Cost'].sum().reset_index()
    fig1 = px.line(costs_over_time, x='Date', y='Total_Daily_Cost', title="Daily Operating Costs Over Time")
    st.plotly_chart(fig1, use_container_width=True)

    # Plot: Occupancy Rate by Shelter Location
    st.subheader("Occupancy Rate by Shelter Location")
    occupancy_by_shelter = filtered_data.groupby('Shelter_Location')['Occupancy_Rate (%)'].mean().reset_index()
    fig2 = px.bar(occupancy_by_shelter, x='Shelter_Location', y='Occupancy_Rate (%)', title="Average Occupancy Rate by Shelter Location")
    st.plotly_chart(fig2, use_container_width=True)

    # Funding Sources Summary
    st.subheader("Funding Sources Overview")
    fig3 = px.pie(funding_sources, values='Funding_Amount', names='Source_Name', title="Funding Sources Breakdown")
    st.plotly_chart(fig3, use_container_width=True)

    # Donor Contributions Summary
    st.subheader("Top Donors")
    top_donors = donors.groupby('Donor_Name')['Donation_Amount'].sum().nlargest(10).reset_index()
    fig4 = px.bar(top_donors, x='Donor_Name', y='Donation_Amount', title="Top 10 Donors")
    st.plotly_chart(fig4, use_container_width=True)

    # Payroll Overview
    st.subheader("Payroll Overview")
    total_payroll = payroll['Total_Compensation'].sum()
    avg_salary = payroll['Salary'].mean()
    
    col5, col6 = st.columns(2)
    col5.metric("Total Payroll", f"${total_payroll:,.2f}")
    col6.metric("Average Salary", f"${avg_salary:,.2f}")

    # Grant Allocations by Purpose
    st.subheader("Grant Allocations by Purpose")
    grant_allocation_by_purpose = grant_allocations.groupby('Purpose')['Allocation_Amount'].sum().reset_index()
    fig5 = px.bar(grant_allocation_by_purpose, x='Purpose', y='Allocation_Amount', title="Grant Allocations by Purpose")
    st.plotly_chart(fig5, use_container_width=True)

    # Utilities Costs Summary
    st.subheader("Utilities Costs")
    utilities_summary = utilities.groupby('Utility_Type')['Utility_Cost'].sum().reset_index()
    fig6 = px.pie(utilities_summary, values='Utility_Cost', names='Utility_Type', title="Utilities Costs Breakdown")
    st.plotly_chart(fig6, use_container_width=True)

    # Footer
    st.markdown("""
    ---
    **Note:** This dashboard provides a comprehensive overview of the financial operations of shelters, funding sources, donor contributions, payroll, grant allocations, and utilities costs for a non-profit organization.
    """)

if __name__ == "__main__":
    main()
