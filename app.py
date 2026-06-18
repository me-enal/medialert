import streamlit as st
import pandas as pd
from data.save_data import load_hospitals
from components.cards import show_hospital_card
from components.map_view import show_map
from components.stats import show_stats
from components.ai_recommender import show_ai_recommender
from components.update_panel import show_update_panel

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="MediAlert",
    page_icon="🚨",
    layout="wide"
)

# ─────────────────────────────────────────
# MINIMAL CSS
# ─────────────────────────────────────────
st.markdown("""
    <style>
        /* Base */
        .main { background-color: #f5f6fa; }
        .stApp { background-color: #f5f6fa; }
        [data-testid="stAppViewContainer"] { background-color: #f5f6fa; }
        [data-testid="stHeader"] { background-color: #ffffff; border-bottom: 1px solid #e9ecef; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e9ecef;
        }

        /* All text dark */
        .stApp p { color: #212529; }
        .stApp label { color: #343a40; }
        .stApp h1, .stApp h2,
        .stApp h3, .stApp h4 { color: #212529; }
        .stCheckbox label { color: #343a40 !important; }
        .stSelectbox label { color: #343a40 !important; }
        .stSlider label { color: #343a40 !important; }
        .stTabs [data-baseweb="tab"] { color: #343a40; font-size:14px; }

        /* Fix all buttons to light */
        .stLinkButton a {
            background-color: #ffffff !important;
            color: #343a40 !important;
            border: 1px solid #dee2e6 !important;
            border-radius: 8px !important;
            font-size: 13px !important;
        }
        .stLinkButton a:hover {
            background-color: #f8f9fa !important;
            border-color: #adb5bd !important;
        }
        .stButton > button {
            background-color: #ffffff !important;
            color: #343a40 !important;
            border: 1px solid #dee2e6 !important;
            border-radius: 8px !important;
            font-size: 13px !important;
        }
        .stButton > button:hover {
            background-color: #f8f9fa !important;
            border-color: #adb5bd !important;
        }

        /* Primary button stays red */
        .stLinkButton a[kind="primary"],
        [data-testid="stLinkButtonContainer"] a {
            background-color: #ffffff !important;
        }

        /* Metric containers */
        div[data-testid="metric-container"] {
            background: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 14px;
        }
        div[data-testid="metric-container"] p { color: #343a40; }
        div[data-testid="metric-container"] label { color: #6c757d; }

        /* Form inputs */
        .stTextInput input {
            background: #ffffff !important;
            color: #212529 !important;
            border: 1px solid #dee2e6 !important;
            border-radius: 8px !important;
        }
        .stSelectbox div {
            color: #212529 !important;
        }

        /* Expander */
        .streamlit-expanderHeader {
            background: #ffffff !important;
            color: #343a40 !important;
            border: 1px solid #e9ecef !important;
            border-radius: 8px !important;
        }

        /* Tab active */
        .stTabs [aria-selected="true"] {
            color: #e63946 !important;
            border-bottom: 2px solid #e63946 !important;
        }
    </style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────
hospitals = load_hospitals()

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    filter_type = st.selectbox(
        "🏥 Hospital Type",
        ["All", "Government", "Private"]
    )

    filter_distance = st.slider(
        "📏 Max Distance (km)",
        min_value=1,
        max_value=20,
        value=15
    )

    st.markdown("### ✅ Must Have")
    filter_beds = st.checkbox("🛏️ Beds Available")
    filter_icu = st.checkbox("🏥 ICU Available")
    filter_oxygen = st.checkbox("🫁 Oxygen Available")
    filter_24h = st.checkbox("⏰ Open 24 Hours")

    st.markdown("### 🩸 Blood Type Needed")
    blood_types = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    blood_filters = {}
    b1, b2 = st.columns(2)
    for i, bt in enumerate(blood_types):
        if i % 2 == 0:
            with b1:
                blood_filters[bt] = st.checkbox(bt, key=f"blood_{bt}")
        else:
            with b2:
                blood_filters[bt] = st.checkbox(bt, key=f"blood_{bt}")

    st.markdown("### ℹ️ Legend")
    st.markdown("""
        <p style="color:#212529">🟢 Good &nbsp;&nbsp; 🟡 Low &nbsp;&nbsp; 🔴 Critical</p>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
        <p style="color:#6c757d; font-size:13px">
            Data updated by hospital staff every 30 mins
        </p>
        <p style="color:#6c757d; font-size:13px">
            🚨 Emergency? Always call <b>108</b> first
        </p>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────
# ─────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────
st.markdown("""
    <div style="
        background: linear-gradient(135deg, #e63946 0%, #c1121f 100%);
        border-radius: 16px;
        padding: 32px 36px;
        margin-bottom: 28px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 6px 20px rgba(230,57,70,0.35);
    ">
        <div>
            <div style="
                font-size: 46px;
                font-weight: 800;
                color: #ffffff;
                letter-spacing: -2px;
                line-height: 1;
            ">🚨 MediAlert</div>
            <div style="
                font-size: 16px;
                color: rgba(255,255,255,0.9);
                margin-top: 8px;
                font-weight: 500;
            ">Real-time hospital resource finder for emergency patients</div>
            <div style="
                font-size: 13px;
                color: rgba(255,255,255,0.7);
                margin-top: 5px;
            ">📍 Showing hospitals near Ludhiana, Punjab</div>
        </div>
        <div style="text-align:right">
            <a href="tel:108" style="
                background: #ffffff;
                color: #e63946;
                padding: 14px 32px;
                border-radius: 50px;
                font-size: 17px;
                font-weight: 800;
                text-decoration: none;
                display: inline-block;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                letter-spacing: 0.5px;
            ">🆘 SOS — Call 108</a>
            <div style="
                font-size: 12px;
                color: rgba(255,255,255,0.6);
                margin-top: 8px;
            ">National Emergency Ambulance</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────
# STATS ROW
# ─────────────────────────────────────────
show_stats(hospitals)

# ─────────────────────────────────────────
# TABS
# ─────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🏥 Hospitals",
    "🤖 AI Recommender",
    "🗺️ Map",
    "🔄 Update Panel"
])

# ─────────────────────────────────────────
# FILTERING LOGIC
# ─────────────────────────────────────────
filtered_hospitals = []
for hospital in hospitals:
    if filter_type != "All" and hospital['type'] != filter_type:
        continue
    if hospital['distance'] > filter_distance:
        continue
    if filter_beds and hospital['beds_available'] == 0:
        continue
    if filter_icu and hospital['icu_available'] == 0:
        continue
    if filter_oxygen and hospital['oxygen_cylinders'] == 0:
        continue
    if filter_24h and not hospital['open_24h']:
        continue
    selected_blood = [bt for bt, checked in blood_filters.items() if checked]
    if selected_blood:
        has_blood = any(
            hospital['blood_bank'].get(bt, False)
            for bt in selected_blood
        )
        if not has_blood:
            continue
    filtered_hospitals.append(hospital)

filtered_hospitals = sorted(
    filtered_hospitals,
    key=lambda x: x['distance']
)

# ─────────────────────────────────────────
# TAB 1 — HOSPITALS
# ─────────────────────────────────────────
with tab1:
    st.markdown(f"#### Found {len(filtered_hospitals)} hospital(s) near you")
    if len(filtered_hospitals) == 0:
        st.warning("No hospitals match your filters. Try adjusting the sidebar filters.")
    else:
        for hospital in filtered_hospitals:
            show_hospital_card(hospital)

# ─────────────────────────────────────────
# TAB 2 — AI RECOMMENDER
# ─────────────────────────────────────────
with tab2:
    show_ai_recommender(hospitals)

# ─────────────────────────────────────────
# TAB 3 — MAP
# ─────────────────────────────────────────
with tab3:
    st.markdown("#### 🗺️ Hospitals Near You")
    st.caption("Green = beds available · Orange = low · Red = full")
    show_map(filtered_hospitals)

# ─────────────────────────────────────────
# TAB 4 — UPDATE PANEL
# ─────────────────────────────────────────
with tab4:
    show_update_panel(hospitals)