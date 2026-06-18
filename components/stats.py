import streamlit as st
import pandas as pd

def show_stats(hospitals):
    df = pd.DataFrame(hospitals)

    total_beds = int(df['beds_available'].sum())
    total_icu = int(df['icu_available'].sum())
    total_oxygen = int(df['oxygen_cylinders'].sum())
    total_doctors = int(df['doctors_on_duty'].sum())
    total_hospitals = len(hospitals)
    open_24h = len([h for h in hospitals if h['open_24h']])

    st.markdown(f"""
        <div style="
            display:grid;
            grid-template-columns:repeat(5,1fr);
            border:1px solid #e9ecef;
            border-radius:10px;
            overflow:hidden;
            margin-bottom:20px;
            background:#ffffff;
            box-shadow:0 2px 8px rgba(0,0,0,0.05);
        ">
            <div style="padding:16px 20px;text-align:center;border-right:1px solid #e9ecef">
                <div style="font-size:13px;color:#343a40;font-weight:700;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px">🛏️ Total Beds Free</div>
                <div style="font-size:36px;font-weight:800;color:#2ecc71">{total_beds}</div>
                <div style="font-size:11px;color:#adb5bd;margin-top:4px">across all hospitals</div>
            </div>
            <div style="padding:16px 20px;text-align:center;border-right:1px solid #e9ecef">
                <div style="font-size:13px;color:#343a40;font-weight:700;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px">🏥 ICU Beds Free</div>
                <div style="font-size:36px;font-weight:800;color:#3498db">{total_icu}</div>
                <div style="font-size:11px;color:#adb5bd;margin-top:4px">across all hospitals</div>
            </div>
            <div style="padding:16px 20px;text-align:center;border-right:1px solid #e9ecef">
               <div style="font-size:13px;color:#343a40;font-weight:700;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px">🫁 Oxygen Cylinders</div>
                <div style="font-size:36px;font-weight:800;color:#9b59b6">{total_oxygen}</div>
                <div style="font-size:11px;color:#adb5bd;margin-top:4px">across all hospitals</div>
            </div>
            <div style="padding:16px 20px;text-align:center;border-right:1px solid #e9ecef">
               <div style="font-size:13px;color:#343a40;font-weight:700;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px">👨‍⚕️ Doctors On Duty</div>
                <div style="font-size:36px;font-weight:800;color:#e67e22">{total_doctors}</div>
                <div style="font-size:11px;color:#adb5bd;margin-top:4px">across all hospitals</div>
            </div>
            <div style="padding:16px 20px;text-align:center;">
                <div style="font-size:13px;color:#343a40;font-weight:700;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px">🏥 Hospitals</div>
                <div style="font-size:36px;font-weight:800;color:#e63946">{total_hospitals}</div>
                <div style="font-size:11px;color:#adb5bd;margin-top:4px">{open_24h} open 24h</div>
            </div>
        </div>
    """, unsafe_allow_html=True)