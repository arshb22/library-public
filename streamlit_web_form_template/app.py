import streamlit as st
import psycopg2
import pandas as pd
import json
from datetime import datetime

# Database connection parameters
DB_HOST = 'your_host'
DB_USER = 'your_user'
DB_PASS = 'your_password'
DB_NAME = 'your_database'

# Function to connect to the PostgreSQL database
def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# Function to insert JSON data into the database
def insert_json_data(form_id, form_data):
    conn = connect_db()
    cur = conn.cursor()
    now = datetime.now()
    data_json = json.dumps(form_data)  # Convert Python dictionary to JSON string
    try:
        cur.execute("INSERT INTO form_data (form_id, data, created_at) VALUES (%s, %s, %s)",
                    (form_id, data_json, now))
        conn.commit()
        log_event("Data inserted", form_data)
    except Exception as e:
        log_event("Error", str(e))
    finally:
        cur.close()
        conn.close()

# Function to log events to the sidebar
def log_event(action, data):
    st.sidebar.write(f"{datetime.now()}: {action} - {data}")

# Main Streamlit UI
def main():
    st.title('Business Evaluation Worksheet')

    # Unique form ID input
    form_id = st.text_input("Form ID", "Enter unique ID for this submission")

    with st.form(key='evaluation_form'):

        st.subheader('A. Recruit and Branch Information')
        col1, col2, col3 = st.columns(3)
        with col1:
            recruit_name = st.text_input('Recruit’s Name', key='recruit_name')
            current_firm = st.text_input('Current Firm', key='current_firm')
            current_firm_other = st.text_input('Current Firm if Other:', key='current_firm_other')
            market_director = st.text_input('Market Director', key='market_director')
            market_executive = st.text_input('Market Executive', key='market_executive')
            wire = st.text_input('Wire', key='wire')
        with col2:
            team_members = st.text_input('Team Members - Name', key='team_members')
            title = st.text_input('Title', key='title')
            external_recruiter_name = st.text_input('External Recruiter Name', key='external_recruiter_name')
            employee_referral_name = st.text_input('Employee Referral Name', key='employee_referral_name')
            trailing_12_quintile = st.text_input('Trailing 12 Quintile:', key='trailing_12_quintile')
            assets_under_mgmt_quintile = st.text_input('Assets Under Mgmt Quintile:', key='assets_under_mgmt_quintile')
            registered_unregistered = st.text_input('Registered/Unregistered', key='registered_unregistered')
        with col3:
            
            licenses = st.text_input('Licenses', key='licenses')
            advisor_discovery_tool = st.checkbox('Was the Advisor Discovery tool used to source your recruit?', key='advisor_discovery_tool')

        st.subheader('B. Production (Non Transferable revenues are backed out of Net T12 Production)')

        submitted = st.form_submit_button("Submit")
        if submitted:
            # Gather all form inputs into a dictionary
            form_data = {
                'recruit_name': recruit_name,
                'current_firm': current_firm,
                'current_firm_other': current_firm_other,
                'market_director': market_director,
                'market_executive': market_executive,
                'wire': wire,
                'team_members': team_members,
                'title': title,
                'external_recruiter_name': external_recruiter_name,
                'employee_referral_name': employee_referral_name,
                'trailing_12_quintile': trailing_12_quintile,
                'assets_under_mgmt_quintile': assets_under_mgmt_quintile,
                'registered_unregistered': registered_unregistered,
                'licenses': licenses,
                'advisor_discovery_tool': advisor_discovery_tool
                # Add other form fields here...
            }
            # Insert form data as JSON into the database
            insert_json_data(form_id, form_data)
            st.write("Form submitted!")

# Run the Streamlit application
if __name__ == "__main__":
    main()
