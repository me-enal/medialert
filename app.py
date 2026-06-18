import streamlit as st
import pandas as pd
from data.save_data import load_hospitals
hospitals = load_hospitals()
from components.cards import show_hospital_card
from components.map_view import show_map
from components.stats import show_stats
from components.update_panel import show_update_panel
from components.ai_recommender import show_ai_recommender

# ─────────────────────────────────────────
# Concept: st.set_page_config — must be the
# FIRST streamlit command in any app
# ─────────────────────────────────────────
st.set_page_config(
    page_title="MediAlert",
    page_icon="🚨",
    layout="wide"
)

# ─────────────────────────────────────────
# Concept: Custom CSS — we can inject CSS
# into Streamlit using st.markdown
# ─────────────────────────────────────────
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        .sos-button {
            background-color: #ff4444;
            color: white;
            font-size: 24px;
            padding: 15px 40px;
            border-radius: 50px;
            border: none;
            cursor: pointer;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(255,68,68,0.7); }
            70% { box-shadow: 0 0 0 15px rgba(255,68,68,0); }
            100% { box-shadow: 0 0 0 0 rgba(255,68,68,0); }
        }
        .header-box {
            background: linear-gradient(135deg, #c0392b, #e74c3c);
            padding: 20px;
            border-radius: 12px;
            color: white;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# Concept: Session State initialization
# Session state persists data between 
# user interactions without resetting
# ─────────────────────────────────────────
if 'selected_hospital' not in st.session_state:
    st.session_state['selected_hospital'] = None

# ─────────────────────────────────────────
# HEADER SECTION
# ─────────────────────────────────────────
st.markdown("""
    <div class="header-box">
        <h1>🚨 MediAlert</h1>
        <p>Real-time hospital resource finder for emergency patients</p>
        <p>📍 Showing hospitals near Ludhiana, Punjab</p>
    </div>
""", unsafe_allow_html=True)

# SOS Button
col_sos, col_info = st.columns([1, 3])
with col_sos:
    st.markdown("""
        <a href="tel:108">
            <button class="sos-button">🆘 SOS — Call 108</button>
        </a>
    """, unsafe_allow_html=True)
with col_info:
    st.info("💡 **Tip:** Use filters below to find hospitals with specific resources. Green = Available, Yellow = Low, Red = Critical.")

st.markdown("---")

# ─────────────────────────────────────────
# FILTERS SECTION
# Concept: Streamlit widgets — interactive
# UI elements that return values we use
# to filter data
# ─────────────────────────────────────────
# MAP SECTION
# AI RECOMMENDER
show_ai_recommender(hospitals)
st.markdown("---")
# STATS DASHBOARD
show_stats(hospitals)
st.markdown("### 🗺️ Hospitals Near You")
show_map(hospitals)
st.markdown("---")
st.markdown("### 🔍 Filter Hospitals")

# Concept: st.columns — side by side layout
f1, f2, f3, f4 = st.columns(4)

with f1:
    # Concept: selectbox — dropdown widget
    filter_type = st.selectbox(
        "🏥 Hospital Type",
        ["All", "Government", "Private"]
    )

with f2:
    # Concept: slider — range input widget
    filter_distance = st.slider(
        "📏 Max Distance (km)",
        min_value=1,
        max_value=20,
        value=15
    )

with f3:
    # Concept: checkbox — boolean toggle widget
    filter_beds = st.checkbox("🛏️ Beds Available")
    filter_icu = st.checkbox("🏥 ICU Available")

with f4:
    filter_oxygen = st.checkbox("🫁 Oxygen Available")
    filter_24h = st.checkbox("⏰ Open 24 Hours")

# Blood type filter
st.markdown("**🩸 Filter by Blood Type:**")
blood_cols = st.columns(8)
blood_types = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
# Concept: Dictionary — storing checkbox values by blood type
blood_filters = {}
for i, bt in enumerate(blood_types):
    with blood_cols[i]:
        blood_filters[bt] = st.checkbox(bt, key=f"blood_{bt}")

st.markdown("---")

# ─────────────────────────────────────────
# FILTERING LOGIC
# Concept: List filtering — we loop through
# hospitals and keep only those that match
# all selected filters
# ─────────────────────────────────────────
filtered_hospitals = []

for hospital in hospitals:
    
    # Filter by type
    if filter_type != "All" and hospital['type'] != filter_type:
        continue
    
    # Filter by distance
    if hospital['distance'] > filter_distance:
        continue
    
    # Filter by beds
    if filter_beds and hospital['beds_available'] == 0:
        continue
    
    # Filter by ICU
    if filter_icu and hospital['icu_available'] == 0:
        continue
    
    # Filter by oxygen
    if filter_oxygen and hospital['oxygen_cylinders'] == 0:
        continue
    
    # Filter by 24h
    if filter_24h and not hospital['open_24h']:
        continue
    
    # Filter by blood type
    # Concept: any() — returns True if at least one item in a list is True
    selected_blood = [bt for bt, checked in blood_filters.items() if checked]
    if selected_blood:
        has_blood = any(hospital['blood_bank'].get(bt, False) for bt in selected_blood)
        if not has_blood:
            continue
    
    filtered_hospitals.append(hospital)

# ─────────────────────────────────────────
# RESULTS SUMMARY
# Concept: f-string — embedding variables
# inside strings using {}
# ─────────────────────────────────────────
st.markdown(f"### 🏥 Found {len(filtered_hospitals)} hospital(s)")

# Sort by distance
# Concept: sorted() with lambda — sorts list
# by a specific key inside each dictionary
filtered_hospitals = sorted(
    filtered_hospitals,
    key=lambda x: x['distance']
)

# ─────────────────────────────────────────
# DISPLAY HOSPITAL CARDS
# Concept: Loop — call show_hospital_card()
# for each hospital in filtered list
# ─────────────────────────────────────────
if len(filtered_hospitals) == 0:
    st.warning("⚠️ No hospitals found matching your filters. Try relaxing the filters.")
else:
    for hospital in filtered_hospitals:
        show_hospital_card(hospital)

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
# UPDATE PANEL
st.markdown("---")
with st.expander("🔄 Hospital Staff — Update Your Data"):
    show_update_panel(hospitals)
st.markdown("---")
st.markdown("""
    <div style='text-align:center; color:gray; font-size:13px'>
        🚨 MediAlert — In a real emergency always call <b>108</b> first<br>
        Data is updated by hospital staff every 30 minutes
    </div>
""", unsafe_allow_html=True)