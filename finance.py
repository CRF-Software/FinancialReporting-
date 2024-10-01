import os
import streamlit as st
import boto3
import pandas as pd
from io import StringIO
from dotenv import load_dotenv

# Load environment variables from .env file (optional, if using a .env file)
load_dotenv()

# Function to load the CSV file from S3 using environment variables
def load_data_from_s3(bucket_name, file_key):
    # Fetch AWS credentials from environment variables
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    # Initialize a session using the environment variables for credentials
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

    # Fetch the CSV file from S3
    response = s3.get_object(Bucket=bucket_name, Key=file_key)

    # Read the CSV file content as a pandas dataframe
    csv_string = response['Body'].read().decode('utf-8')
    data = pd.read_csv(StringIO(csv_string))
    
    return data

# Main Streamlit App
def main():
    st.title("Financial Data from S3")

    # Get the bucket name and file key from the user
    bucket_name = st.text_input("Enter S3 Bucket Name")
    file_key = st.text_input("Enter S3 File Key (path to the CSV file)")

    if bucket_name and file_key:
        try:
            # Load the data from S3
            data = load_data_from_s3(bucket_name, file_key)
            
            # Display the dataset summary
            st.write("### Dataset Summary")
            st.write(data.describe())
            
            # Display the data
            st.write("### Financial Data")
            st.dataframe(data)
        except Exception as e:
            st.error(f"Error loading data from S3: {e}")

if __name__ == "__main__":
    main()
