import streamlit as st
import pandas as pd
import os
from base64 import b64encode

def process_csv_files(csv_files, num_columns):
    # Initialize progress message
    progress_text = st.empty()
    
    # Initialize empty list to store DataFrames
    dataframes = []
    
    # Loop through each CSV file
    for csv_file in csv_files:
        progress_text.text(f"Processing file: {csv_file.name}")
        
        # Read CSV file
        df = pd.read_csv(csv_file)
        
        # Extract specified number of columns
        df = df.iloc[:, :num_columns]
        
        # Add filename as a column
        df['Filename'] = csv_file.name
        
        # Append to list
        dataframes.append(df)
    
    # Concatenate all DataFrames
    data = pd.concat(dataframes, ignore_index=True)
    
    progress_text.text("Data processing complete!")
    return data

def main():
    st.title("CSV Data Extraction Tool")
    
    # File selection
    csv_files = st.sidebar.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)
    
    # Number of columns input
    num_columns = st.sidebar.number_input("Number of columns to copy:", min_value=1, step=1, value=18)
    
    # Process button
    if st.sidebar.button("Process Data"):
        if not csv_files:
            st.warning("Please upload one or more CSV files.")
        else:
            data = process_csv_files(csv_files, num_columns)
            st.write("Extracted Data:")
            st.write(data)
            
            # Create a download link for the consolidated data with icons
            csv = data.to_csv(index=False)
            b64_csv = b64encode(csv.encode()).decode()
            href = f'data:text/csv;base64,{b64_csv}'
            download_text = f'<a href="{href}" download="consolidated_data.csv"><img src="https://raw.githubusercontent.com/streamlit/streamlit/develop/packages/streamlit/assets/filebrowser/download.png"/></a>'
            st.markdown(download_text, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
