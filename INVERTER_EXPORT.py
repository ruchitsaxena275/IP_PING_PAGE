import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of all 80 inverter IPs in order.
inverter_ips = [
    '10.22.250.2','10.22.250.3','10.22.250.4','10.22.250.5',
    # ... Add the rest from your list ...
    '10.22.250.214'
]

def get_export_value(ip):
    try:
        url = f"http://{ip}"  # Adjust if a specific port or path is needed, e.g. /main or /status
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # The export value is in a div with class 'label_top_num'
        result = soup.find('span', {'class': 'label_top_num'})
        return result.text.strip() if result else 'N/A'
    except Exception as e:
        return 'Error'

# Organize the results
results = []
for i, ip in enumerate(inverter_ips):
    itc = f"ITC {i//4 + 1}"
    inverter = f"Inverter {i%4 + 1}"
    export_value = get_export_value(ip)
    results.append({"ITC": itc, "Inverter": inverter, "IP": ip, "Export Value": export_value})

# Create DataFrame and Streamlit UI
df = pd.DataFrame(results)

st.title('Inverter Export Value Dashboard')
st.dataframe(df)
