import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="IPAS Executive Dashboard", layout="wide")

# Premium CSS
st.markdown("""
    <style>
    .stApp { background-color: #F7F3EC; }
    .header { background: linear-gradient(135deg, #004D33, #00704A); padding: 30px; border-radius: 15px; color: white; text-align: center; border-bottom: 5px solid #C8973A; }
    div[data-testid="metric-container"] { background: white; border-radius: 12px; padding: 15px; border-top: 5px solid #00704A; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    </style>
    <div class="header"><h1>🏛️ IPAS INTELLIGENCE ENGINE</h1><p>Ministry of Planning & Development | DevOps Ready</p></div>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.header("📂 Data Source")
    file = st.file_uploader("Upload PC-1 Excel", type=['xlsx'])

if file:
    df = pd.read_excel(file)
    # Cost Cleaning Logic
    cost_col = next((c for c in df.columns if any(k in str(c).lower() for k in ['cost', 'amount', 'budget', 'pkr'])), None)
    if cost_col:
        df[cost_col] = pd.to_numeric(df[cost_col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        total_b = df[cost_col].sum() / 1e9
    
    k1, k2, k3 = st.columns(3)
    k1.metric("TOTAL PROJECTS", len(df))
    k2.metric("PORTFOLIO (BILLION)", f"{total_b:.2f} B" if cost_col else "0")
    k3.metric("SYSTEM STATUS", "Operational")

    st.plotly_chart(px.pie(df, hole=0.6, color_discrete_sequence=['#004D33', '#C8973A']), use_container_width=True)
    
    # Export Button for Seniors
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Cleaned CSV", csv, "Report.csv", "text/csv")
else:
    st.info("Please upload Excel file to start.")