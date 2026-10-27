import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.analysis import load_data, overall_kpis, grouped_performance, daily_performance

st.set_page_config(page_title="E-Commerce Conversion Analytics", page_icon="🛒", layout="wide")
st.title("🛒 E-Commerce Conversion Rate Analytics")
st.caption("Python • Pandas • NumPy • Matplotlib • Streamlit • MySQL")
st.info("This project uses synthetic demo data for learning and portfolio practice.")
@st.cache_data
def get_data():
    return load_data("data/sessions.csv")
df = get_data()

with st.sidebar:
    st.header("Filters")
    min_date, max_date = df.session_date.min().date(), df.session_date.max().date()
    date_range = st.date_input("Date range", value=(min_date,max_date), min_value=min_date, max_value=max_date)
    devices = st.multiselect("Device", sorted(df.device.unique()), default=sorted(df.device.unique()))
    channels = st.multiselect("Channel", sorted(df.channel.unique()), default=sorted(df.channel.unique()))
    countries = st.multiselect("Country", sorted(df.country.unique()), default=sorted(df.country.unique()))
    pages = st.multiselect("Landing page", sorted(df.landing_page.unique()), default=sorted(df.landing_page.unique()))

f = df[df.device.isin(devices) & df.channel.isin(channels) & df.country.isin(countries) & df.landing_page.isin(pages)].copy()
if isinstance(date_range,(tuple,list)) and len(date_range)==2:
    f = f[f.session_date.dt.date.between(date_range[0],date_range[1])]
if f.empty:
    st.warning("No data matches these filters. Adjust the sidebar filters.")
    st.stop()
k = overall_kpis(f)
cols = st.columns(5)
for col, label, value in zip(cols, ["Sessions","Conversions","Conversion rate","Revenue","Average order value"],
    [f'{k["sessions"]:,}',f'{k["conversions"]:,}',f'{k["conversion_rate"]:.2f}%',f'${k["revenue"]:,.2f}',f'${k["average_order_value"]:,.2f}']):
    col.metric(label,value)

a,b = st.columns(2)
with a:
    st.subheader("Conversion rate by channel")
    x = grouped_performance(f,"channel").sort_values("conversion_rate",ascending=False)
    fig,ax=plt.subplots(); ax.bar(x.channel,x.conversion_rate); ax.set_ylabel("Conversion rate (%)")
    ax.tick_params(axis="x",rotation=35); fig.tight_layout(); st.pyplot(fig); plt.close(fig)
with b:
    st.subheader("Sessions and conversions over time")
    x=daily_performance(f); fig,ax=plt.subplots()
    ax.plot(pd.to_datetime(x.date),x.sessions,label="Sessions"); ax.plot(pd.to_datetime(x.date),x.conversions,label="Conversions")
    ax.legend(); fig.autofmt_xdate(); fig.tight_layout(); st.pyplot(fig); plt.close(fig)
a,b=st.columns(2)
with a:
    st.subheader("Conversion rate by device")
    x=grouped_performance(f,"device"); fig,ax=plt.subplots(); ax.bar(x.device,x.conversion_rate)
    ax.set_ylabel("Conversion rate (%)"); fig.tight_layout(); st.pyplot(fig); plt.close(fig)
with b:
    st.subheader("Revenue by landing page")
    x=grouped_performance(f,"landing_page").sort_values("revenue",ascending=False)
    fig,ax=plt.subplots(); ax.bar(x.landing_page,x.revenue); ax.set_ylabel("Revenue ($)")
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)

st.subheader("Performance breakdown")
dimension=st.selectbox("Group by",["channel","device","country","landing_page"])
st.dataframe(grouped_performance(f,dimension).round(2),use_container_width=True,hide_index=True)
st.subheader("Explore sessions")
search=st.text_input("Search session ID")
view=f[f.session_id.str.contains(search,case=False,na=False)] if search else f
st.dataframe(view,use_container_width=True,hide_index=True)
st.download_button("Download filtered CSV",view.to_csv(index=False).encode(), "filtered_sessions.csv","text/csv")
st.caption("Conversion rate = conversions / sessions × 100. AOV = revenue / conversions.")
