import streamlit as st
import subprocess
import platform
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="IP Ping Monitor", layout="wide")
st.title("🌐 IP Ping Monitor (Cloud-Safe Version)")

ip_list = ['8.8.8.8', '8.8.4.4', '1.1.1.1', '192.168.1.1', '192.168.0.1', '10.0.0.1', '172.16.0.1', '192.168.10.1', '192.168.100.1', '192.168.1.254', '192.168.0.254', '10.10.10.10', '10.1.1.1', '192.168.2.1', '192.168.50.1']

def ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(["ping", param, "1", host],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                timeout=3)
        if result.returncode == 0:
            output = result.stdout
            if platform.system().lower() == "windows":
                idx = output.find("time=")
                if idx != -1:
                    time_str = output[idx+5:].split("ms")[0].strip()
                    return "✅ Online", int(float(time_str))
            else:
                idx = output.find("time=")
                if idx != -1:
                    time_str = output[idx+5:].split(" ms")[0].strip()
                    return "✅ Online", int(float(time_str))
            return "✅ Online", None
        else:
            return "❌ Offline", None
    except subprocess.TimeoutExpired:
        return "❌ Offline", None
    except Exception:
        return "❌ Offline", None

status_data = []
for ip in ip_list:
    status, response_time = ping(ip)
    if response_time:
        status_display = f"{status} ({response_time} ms)"
    else:
        status_display = status
    status_data.append({"IP": ip, "Status": status_display, "Checked At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

df = pd.DataFrame(status_data)
st.dataframe(df, use_container_width=True)

if st.button("🔄 Refresh Status"):
    st.experimental_rerun()
