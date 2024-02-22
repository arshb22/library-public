import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def validate_dataframe(df):
    """Validate the DataFrame to ensure it contains 'GPN' and 'effective month'."""
    required_columns = {'FA_GPN', 'Effective_Month'}
    if not required_columns.issubset(df.columns):
        return False
    return True

def generate_pdf(df):
    """Generate a PDF from a DataFrame."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    # Simple text output of DataFrame's content for now, need to adapt this to fit the actual model output or whatever PDFs 
    text_obj = c.beginText(40, height - 40)
    text_obj.setFont("Helvetica", 10)
    for index, row in df.iterrows():
        text_line = ', '.join(str(value) for value in row)
        text_obj.textLine(text_line)
    c.drawText(text_obj)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


def process_data(df):
    """Add model logic here to return the plots we need"""
    # Implement your logic
    return df

st.title('File Upload Template')

# File uploader allows user to add their own CSV
uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file is not None:
    # Try to read the uploaded file
    try:
        data = pd.read_csv(uploaded_file)

        # Validate the DataFrame
        if not validate_dataframe(data):
            st.error('The uploaded file does not contain the required columns: GPN and effective month.')
        else:
            # Data processing logic here
            processed_data = process_data(data)
            
            # Dropdown to select a GPN
            gpn_values = processed_data['FA_GPN'].unique()
            selected_gpn = st.selectbox('Select a GPN', gpn_values)
            
            # Filter data based on selected GPN and display
            filtered_data = processed_data[processed_data['FA_GPN'] == selected_gpn]
            st.write(filtered_data)
            pdf_bytes = generate_pdf(filtered_data)
            st.download_button(
                label="Download PDF for selected GPN",
                data=pdf_bytes,
                file_name=f"{selected_gpn}_data.pdf",
                mime='application/pdf',
            )
            
            # Generate and download PDF for the entire dataset
            entire_pdf_bytes = generate_pdf(processed_data)
            st.download_button(
                label="Download PDF for entire dataset",
                data=entire_pdf_bytes,
                file_name="entire_dataset.pdf",
                mime='application/pdf',
            )

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info('Please upload a CSV file to proceed.')