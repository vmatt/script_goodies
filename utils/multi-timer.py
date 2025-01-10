import streamlit as st
import time
from datetime import datetime, timedelta

# Initialize session state variables if not already done
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'lap_times' not in st.session_state:
    st.session_state.lap_times = [{} for _ in range(20)]

# Function to format time as hh:mm:ss
def format_time(seconds):
    return str(timedelta(seconds=seconds))

def get_elapsed_time(start_time):
    return (datetime.now() - start_time).total_seconds()

# Start Timer button
if st.button("Start Timer") and st.session_state.start_time is None:
    st.session_state.start_time = datetime.now()

# Display current timer if started
if st.session_state.start_time:
    elapsed_time = get_elapsed_time(st.session_state.start_time)
    st.write(f"Total Elapsed Time: {format_time(elapsed_time)}")

    for idx in range(20):
        if st.session_state.lap_times[idx] == {} and st.button(f"Record Time for Person {idx + 1}"):
            st.session_state.lap_times[idx] = {'time': get_elapsed_time(st.session_state.start_time), 'recorded_at': datetime.now()}

# Display recorded times
st.write("Recorded Times:")
for idx, lap in enumerate(st.session_state.lap_times):
    if lap:
        st.write(f"Person {idx + 1}: {format_time(lap['time'])} (recorded at {lap['recorded_at']})")

# Reset button
if st.button("Reset Timers"):
    st.session_state.start_time = None
    st.session_state.lap_times = [{} for _ in range(20)]
