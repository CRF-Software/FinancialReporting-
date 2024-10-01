import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Function to load the CSV file from GitHub
def load_data_from_github(file_url):
    data = pd.read_csv(file_url)
    return data

# Function to filter data by a date range
def filter_data_by_date(data, date_column, start_date, end_date):
    filtered_data = data[(data[date_column] >= pd.to_datetime(start_date)) & 
                         (data[date_column] <= pd.to_datetime(end_date))]
    return filtered_data

# Main Streamlit App
def main():
    st.set_page_config(page_title="Financial Reporting Dashboard", layout="wide")
    
    # Page Title
    st.title("Professional Financial Reporting Dashboard")

    # Hardcoded GitHub raw file URL
    file_url = "https://github.com/CRF-Software/FinancialReporting-/blob/main/financial_sample_data.csv"

    # Load the data from GitHub
    try:
        data = load_data_from_github(file_url)

        # Display a summary of the dataset
        st.write("### Dataset Overview")
        st.write(data.describe())

        # Display the data in a table (with optional filter)
        st.write("### Financial Data (Raw Table)")
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
            filtered_data = filter_data_by_date(data, date_column, start_date, end_date)
            st.write(f"### Filtered Data from {start_date} to {end_date}")
            st.dataframe(filtered_data)

        # Create comparison visuals between two columns
        numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()

        st.write("### Comparative Visualizations")

        # Create columns for comparison selection
        col1, col2 = st.columns(2)

        with col1:
            x_column = st.selectbox("Select X-Axis for Comparison", options=numeric_columns)

        with col2:
            y_column = st.selectbox("Select Y-Axis for Comparison", options=numeric_columns)

        # Create side-by-side visualizations
        col1, col2 = st.columns(2)

        with col1:
            # Generate a scatter plot
            st.write(f"### Scatter Plot: {y_column} vs {x_column}")
            fig = px.scatter(filtered_data, x=x_column, y=y_column, title=f"{y_column} vs {x_column}")
            st.plotly_chart(fig)

        with col2:
            # Generate a histogram
            st.write(f"### Histogram of {y_column}")
            fig = px.histogram(filtered_data, x=y_column, nbins=20, title=f"Distribution of {y_column}")
            st.plotly_chart(fig)

        # Generate a combined line plot
        st.write(f"### Combined Line Chart for {x_column} and {y_column}")
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Plot x_column on primary y-axis
        fig.add_trace(go.Scatter(x=filtered_data[date_column], y=filtered_data[x_column],
                                 mode='lines', name=f'{x_column}', line=dict(color='blue')),
                      secondary_y=False)

        # Plot y_column on secondary y-axis
        fig.add_trace(go.Scatter(x=filtered_data[date_column], y=filtered_data[y_column],
                                 mode='lines', name=f'{y_column}', line=dict(color='green')),
                      secondary_y=True)

        fig.update_layout(title=f"{x_column} and {y_column} Over Time")
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text=f"{x_column}", secondary_y=False)
        fig.update_yaxes(title_text=f"{y_column}", secondary_y=True)

        st.plotly_chart(fig)

        # Add a heatmap comparison
        st.write(f"### Correlation Heatmap for Numerical Data")
        corr_matrix = filtered_data[numeric_columns].corr()

        fig = px.imshow(corr_matrix, text_auto=True, title="Correlation Heatmap", aspect="auto")
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error loading data: {e}")

if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Function to load the CSV file from GitHub
def load_data_from_github(file_url):
    data = pd.read_csv(file_url)
    return data

# Function to filter data by a date range
def filter_data_by_date(data, date_column, start_date, end_date):
    filtered_data = data[(data[date_column] >= pd.to_datetime(start_date)) & 
                         (data[date_column] <= pd.to_datetime(end_date))]
    return filtered_data

# Main Streamlit App
def main():
    st.set_page_config(page_title="Financial Reporting Dashboard", layout="wide")
    
    # Page Title
    st.title("Professional Financial Reporting Dashboard")

    # Hardcoded GitHub raw file URL
    file_url = "https://raw.githubusercontent.com/CRF-Software/FinancialReporting-/main/tcrg-rgat.csv"

    # Load the data from GitHub
    try:
        data = load_data_from_github(file_url)

        # Display a summary of the dataset
        st.write("### Dataset Overview")
        st.write(data.describe())

        # Display the data in a table (with optional filter)
        st.write("### Financial Data (Raw Table)")
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
            filtered_data = filter_data_by_date(data, date_column, start_date, end_date)
            st.write(f"### Filtered Data from {start_date} to {end_date}")
            st.dataframe(filtered_data)

        # Create comparison visuals between two columns
        numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()

        st.write("### Comparative Visualizations")

        # Create columns for comparison selection
        col1, col2 = st.columns(2)

        with col1:
            x_column = st.selectbox("Select X-Axis for Comparison", options=numeric_columns)

        with col2:
            y_column = st.selectbox("Select Y-Axis for Comparison", options=numeric_columns)

        # Create side-by-side visualizations
        col1, col2 = st.columns(2)

        with col1:
            # Generate a scatter plot
            st.write(f"### Scatter Plot: {y_column} vs {x_column}")
            fig = px.scatter(filtered_data, x=x_column, y=y_column, title=f"{y_column} vs {x_column}")
            st.plotly_chart(fig)

        with col2:
            # Generate a histogram
            st.write(f"### Histogram of {y_column}")
            fig = px.histogram(filtered_data, x=y_column, nbins=20, title=f"Distribution of {y_column}")
            st.plotly_chart(fig)

        # Generate a combined line plot
        st.write(f"### Combined Line Chart for {x_column} and {y_column}")
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Plot x_column on primary y-axis
        fig.add_trace(go.Scatter(x=filtered_data[date_column], y=filtered_data[x_column],
                                 mode='lines', name=f'{x_column}', line=dict(color='blue')),
                      secondary_y=False)

        # Plot y_column on secondary y-axis
        fig.add_trace(go.Scatter(x=filtered_data[date_column], y=filtered_data[y_column],
                                 mode='lines', name=f'{y_column}', line=dict(color='green')),
                      secondary_y=True)

        fig.update_layout(title=f"{x_column} and {y_column} Over Time")
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text=f"{x_column}", secondary_y=False)
        fig.update_yaxes(title_text=f"{y_column}", secondary_y=True)

        st.plotly_chart(fig)

        # Add a heatmap comparison
        st.write(f"### Correlation Heatmap for Numerical Data")
        corr_matrix = filtered_data[numeric_columns].corr()

        fig = px.imshow(corr_matrix, text_auto=True, title="Correlation Heatmap", aspect="auto")
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error loading data: {e}")

if __name__ == "__main__":
    main()
