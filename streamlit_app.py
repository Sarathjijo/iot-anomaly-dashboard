import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="IoT Anomaly Dashboard", page_icon="📡", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #11161B; }
h1 { font-family: Georgia, serif; color: #E8EDF2; }
p, label, .stMarkdown { color: #B8C2CC; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load():
    df = pd.read_csv('anomaly_results.csv', parse_dates=['timestamp'])
    return df

df = load()

st.title("Industrial IoT Anomaly Dashboard")
st.write("Pump sensor monitoring. Red points are readings flagged as anomalous by the Isolation Forest model.")

# summary metrics
c1, c2, c3 = st.columns(3)
c1.metric("Total readings", f"{len(df):,}")
c2.metric("Anomalies flagged", f"{df['is_anomaly'].sum():,}")
c3.metric("Anomaly rate", f"{df['is_anomaly'].mean()*100:.1f}%")

st.divider()

# controls
sensors = [c for c in df.columns if c.startswith('sensor_')]
col1, col2 = st.columns([1,2])
with col1:
    sensor = st.selectbox("Sensor", sensors)
    show_breakdowns = st.checkbox("Mark real breakdowns", value=True)

# plot
fig, ax = plt.subplots(figsize=(12,5))
ax.plot(df['timestamp'], df[sensor], color='#4C9BE8', linewidth=0.6, label=sensor)
anom = df[df['is_anomaly']==1]
ax.scatter(anom['timestamp'], anom[sensor], color='#FF5252', s=10, label='Anomaly', zorder=5)

if show_breakdowns:
    broken = df[df['machine_status']=='BROKEN']
    for t in broken['timestamp']:
        ax.axvline(t, color='white', linestyle='--', linewidth=1, alpha=0.7)

ax.set_xlabel("Time"); ax.set_ylabel(f"{sensor} reading")
ax.legend(loc='upper right')
ax.set_facecolor('#11161B'); fig.patch.set_facecolor('#11161B')
ax.tick_params(colors='#B8C2CC'); ax.xaxis.label.set_color('#B8C2CC'); ax.yaxis.label.set_color('#B8C2CC')
for s in ax.spines.values(): s.set_color('#33404A')
st.pyplot(fig)

st.divider()

# anomaly rate by status
st.subheader("Anomaly rate by machine status")
rate = (df.groupby('machine_status')['is_anomaly'].mean()*100).round(1)
st.bar_chart(rate)
st.caption("Anomalies concentrate during BROKEN and RECOVERING periods, confirming the unsupervised model tracks real failures.")
