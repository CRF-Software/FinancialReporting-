import os
import streamlit as st
import pandas as pd

# Function to load the CSV file from GitHub
def load_data_from_github(https://github.com/CRF-Software/FinancialReporting-/blob/main/tcrg-rgat.csv):
    # Read the CSV file content as a pandas dataframe
    data = pd.read_csv(https://github.com/CRF-Software/FinancialReporting-/blob/main/tcrg-rgat.csv)
    return data

# Main Streamlit App
def main():
    st.title("Financial Data from GitHub")

    # Get the GitHub raw file URL from the user
    file_url = st.text_input("https://github.com/CRF-Software/FinancialReporting-/blob/main/tcrg-rgat.csv")

    if file_url:
        try:
            # Load the data from GitHub
            data = load_data_from_github(file_url)
            
            # Display the dataset summary
            st.write("### Dataset Summary")
            st.write(data.describe())
            
            # Display the data
            st.write("### Financial Data")
            st.dataframe(data)
        except Exception as e:
            st.error(f"Error loading data from GitHub: {e}")

if __name__ == "__main__":
    main()
