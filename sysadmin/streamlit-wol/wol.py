import datetime
import streamlit as st
import pandas as pd
import subprocess
import platform
import json
from pathlib import Path

from datetime import datetime, timedelta
from wakeonlan import send_magic_packet


def ping_host(ip):
    # Determine the platform/os and set appropriate ping parameters
    if platform.system().lower() == 'windows':
        # Windows expects timeout in milliseconds
        param = '-w'
        timeout = '500'  # 500 ms
    else:
        # Linux and macOS expect timeout in seconds (accepts decimal)
        param = '-W'
        timeout = '1'  # 0.5 seconds

    command = ['ping', ip, param, timeout, '-c', '1'] if platform.system().lower() != 'windows' else ['ping', ip, param,
                                                                                                      timeout]
    print(command)
    response = subprocess.run(command, capture_output=True, text=True)
    return response.returncode == 0

def load_status_cache():
    try:
        if Path("status_cache.json").exists():
            with open("status_cache.json", "r") as file:
                status_cache = json.load(file)
            return status_cache
    except Exception as e:
        print(f"Failed to load status cache: {e}")
    return {}

def save_status_cache(status_cache):
    try:
        with open("status_cache.json", "w") as file:
            json.dump(status_cache, file)
    except Exception as e:
        print(f"Failed to save status cache: {e}")

def cache_is_valid(status_cache, key):
    if key in status_cache:
        cache_time = datetime.fromisoformat(status_cache[key]["timestamp"])
        if (datetime.now() - cache_time).total_seconds() < 5:
            return True
    return False

def update_status(df, status_dict):
    status_cache = load_status_cache()
    for index, row in df.iterrows():
        ip = row['IP']
        cname = row['Computer Name']
        cache_key = f"{cname}:{ip}"
        if not cache_is_valid(status_cache, cache_key):
            print(f"{datetime.now()}: Pinging {cname} at {ip}")
            status = "Online" if ping_host(ip) else "Offline"
            status_cache[cache_key] = {"status": status, "timestamp": datetime.now().isoformat()}
            st.session_state['last_update'] = datetime.now()
        else:
            print(f"{datetime.now()}: Using cached status for {cname}")
            status = status_cache[cache_key]["status"]
        status_dict[cname] = status
    save_status_cache(status_cache)

def wake_computer(mac, computer_name):
    send_magic_packet(mac)
    # Update the session state for this computer to "Starting..."
    st.session_state['status_cache'][computer_name] = "Starting..."
    # Optional: You might also manually trigger a status update or wait until the next automatic update

# Reading CSV
@st.cache_data
def load_data():
    return pd.read_csv("computers.csv")



# Store the last run time in session state
if 'last_run' not in st.session_state:
    st.session_state.last_run = datetime.now() - timedelta(minutes=1)  # Ensure first run is way back

if 'status_cache' not in st.session_state:
    st.session_state['status_cache'] = {}
status_dict = st.session_state['status_cache']
df = load_data()
update_status(df,status_dict)

# Streamlit layout
st.title('KOL-LAB Wake On Lan')
st.button("Refresh Status", on_click=update_status)
# Placeholder for displaying information
status_placeholder = st.text("To check, hit the refresh status button!")

for index, row in df.iterrows():
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    with col1:
        st.text(row['Computer Name'])
    with col2:
        status_col = st.session_state['status_cache'].get(row['Computer Name'], "Unknown")

        # Rendering based on the current status
        if status_col == "Starting...":
            st.warning(status_col)  # Assuming you want this to be highlighted as a warning or another color
        elif status_col == "Online":
            st.success(status_col)
        elif status_col == "Offline":
            st.error(status_col)
        else:
            st.warning(status_col)
    with col3:
        st.text(row['IP'])
    with col4:
        # Ensure you pass the computer name to the wake function
        if st.button('Wake', key=row['Computer Name']):
            wake_computer(row['MAC Address'], row['Computer Name'])


