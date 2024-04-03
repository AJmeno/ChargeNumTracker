import streamlit as st
import pandas as pd
import datetime
import time

# Set page configuration
st.set_page_config(page_title="Charge Number Tracker", layout="wide")

# Initialize session state
if 'charge_numbers' not in st.session_state:
    st.session_state['charge_numbers'] = pd.DataFrame(columns=['Issue Number', 'Charge Number', 'Date', 'Time Spent (hours)', 'Status'])

if 'active_charge_number' not in st.session_state:
    st.session_state['active_charge_number'] = None

if 'timer_start' not in st.session_state:
    st.session_state['timer_start'] = None

# Function to add a new charge number entry
def add_charge_number():
    issue_number = st.text_input("Issue Number")
    charge_number = st.text_input("Charge Number")
    date = st.date_input("Date")
    time_spent = st.number_input("Time Spent (hours)", min_value=0.0, step=0.1)
    status = st.selectbox("Status", ["", "Approved", "Rejected"])

    if st.button("Add"):
        new_entry = pd.DataFrame({'Issue Number': [issue_number], 'Charge Number': [charge_number], 'Date': [date], 'Time Spent (hours)': [time_spent], 'Status': [status]})
        st.session_state['charge_numbers'] = pd.concat([st.session_state['charge_numbers'], new_entry], ignore_index=True)
        st.success("Charge number entry added!")

# Function to start/stop the timer
def start_stop_timer():
    if st.session_state['active_charge_number'] is None:
        issue_number = st.text_input("Enter Issue Number")
        charge_number = st.text_input("Enter Charge Number to start timer")
        if st.button("Start Timer"):
            st.session_state['active_charge_number'] = charge_number
            st.session_state['timer_start'] = time.time()
            st.success(f"Timer started for charge number: {charge_number}")
    else:
        if st.button("Stop Timer"):
            time_spent = time.time() - st.session_state['timer_start']
            new_entry = pd.DataFrame({'Issue Number': [issue_number], 'Charge Number': [st.session_state['active_charge_number']], 'Date': [datetime.date.today()], 'Time Spent (hours)': [time_spent / 3600], 'Status': ["Approved"]})
            st.session_state['charge_numbers'] = pd.concat([st.session_state['charge_numbers'], new_entry], ignore_index=True)
            st.session_state['active_charge_number'] = None
            st.session_state['timer_start'] = None
            st.success("Timer stopped and entry added!")

# Display the charge number entries
st.subheader("Charge Number Entries")
if not st.session_state['charge_numbers'].empty:
    # Calculate the percentage of time spent on each charge number
    st.session_state['charge_numbers']['Percentage of 8 Hours'] = (st.session_state['charge_numbers']['Time Spent (hours)'] / 8) * 100
    
    # Move the 'Status' column to the end
    cols = st.session_state['charge_numbers'].columns.tolist()
    cols = cols[:4] + cols[-1:] + cols[4:-1]
    st.session_state['charge_numbers'] = st.session_state['charge_numbers'][cols]
    
    # Display the data frame with the percentage column and enable editing
    if st.button("Edit Table"):
        st.session_state['charge_numbers'] = st.experimental_data_editor(st.session_state['charge_numbers'])
    
    # Add a new column to display the status in color
    st.session_state['charge_numbers']['Status'] = st.session_state['charge_numbers']['Status'].apply(lambda x: f'<span style="color:{"green" if x == "Approved" else "red"}">{x}</span>' if x else '')
    st.write(st.session_state['charge_numbers'].to_html(escape=False), unsafe_allow_html=True)
else:
    st.write("No charge number entries yet.")

# Display the bar chart
st.subheader("Time Spent by Charge Number")
if not st.session_state['charge_numbers'].empty:
    charge_number_data = st.session_state['charge_numbers'].groupby('Charge Number')['Time Spent (hours)'].sum().reset_index()
    st.bar_chart(charge_number_data, x='Charge Number', y='Time Spent (hours)')
else:
    st.write("No data available to display the bar chart.")

# Add a new charge number entry
st.subheader("Add a New Charge Number Entry")
add_charge_number()

# Start/stop the timer
st.subheader("Timer")
start_stop_timer()
