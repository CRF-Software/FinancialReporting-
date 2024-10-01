import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load the CSV file from GitHub
def load_data_from_github(file_url):
    # Read the CSV file content as a pandas dataframe
    data = pd.read_csv(file_url)
    return data

# Function to filter data by a date range
def filter_data_by_date(data, date_column, start_date, end_date):
    filtered_data = data[(data[date_column] >= pd.to_datetime(start_date)) & 
                         (data[date_column] <= pd.to_datetime(end_date))]
    return filtered_data

# Main Streamlit App
def main():
    st.title("Financial Data Visualization")

    # Hardcoded GitHub raw file URL
    file_url = "https://raw.githubusercontent.com/CRF-Software/FinancialReporting-/main/tcrg-rgat.csv"

    # Load the data from GitHub
    try:
        data = load_data_from_github(file_url)

        # Display a summary of the dataset
        st.write("### Dataset Summary")
        st.write(data.describe())

        # Display the data in a table
        st.write("### Full Dataset")
        st.dataframe(data)

        # Convert any potential date columns to datetime format
        date_columns = [col for col in data.columns if 'date' in col.lower()]
        for col in date_columns:
            data[col] = pd.to_datetime(data[col], errors='coerce')

        # Allow users to select a date range to filter the data
        if date_columns:
            date_column = st.selectbox("Select Date Column", date_columns)
            min_date = data[date_column].min()
            max_date = data[date_column].max()

            start_date = st.date_input("Start Date", min_date)
            end_date = st.date_input("End Date", max_date)

            # Filter the data by the selected date range
            data = filter_data_by_date(data, date_column, start_date, end_date)
            st.write(f"### Filtered Data from {start_date} to {end_date}")
            st.dataframe(data)

        # Select columns for visualization
        numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
        st.write("### Visualization Options")

        # Choose x-axis and y-axis columns for plotting
        x_column = st.selectbox("Select X-Axis Column", options=numeric_columns)
        y_column = st.selectbox("Select Y-Axis Column", options=numeric_columns)

        # Generate a line chart
        st.write(f"### Line Chart: {y_column} vs {x_column}")
        fig = px.line(data, x=x_column, y=y_column, title=f"{y_column} over {x_column}")
        st.plotly_chart(fig)

        # Generate a scatter plot
        st.write(f"### Scatter Plot: {y_column} vs {x_column}")
        fig = px.scatter(data, x=x_column, y=y_column, title=f"{y_column} vs {x_column}")
        st.plotly_chart(fig)

        # Generate a bar chart
        st.write(f"### Bar Chart: {y_column} vs {x_column}")
        fig = px.bar(data, x=x_column, y=y_column, title=f"{y_column} Bar Chart by {x_column}")
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error loading data: {e}")

if __name__ == "__main__":
    main()
