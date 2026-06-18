import streamlit as st
import pandas as pd

EMERGENCY_WEIGHTS = {
    "Cardiac Arrest": {
        "beds": 0.2,
        "icu": 0.4,
        "doctors": 0.3,
        "oxygen": 0.1,
        "specialization": "Cardiology"
    },
    "Road Accident / Trauma": {
        "beds": 0.3,
        "icu": 0.3,
        "doctors": 0.3,
        "oxygen": 0.1,
        "specialization": "Trauma"
    },
    "Breathing Problem": {
        "beds": 0.2,
        "icu": 0.2,
        "doctors": 0.2,
        "oxygen": 0.4,
        "specialization": "General"
    },
    "Brain / Neuro": {
        "beds": 0.2,
        "icu": 0.4,
        "doctors": 0.3,
        "oxygen": 0.1,
        "specialization": "Neurology"
    },
    "Child Emergency": {
        "beds": 0.3,
        "icu": 0.3,
        "doctors": 0.3,
        "oxygen": 0.1,
        "specialization": "Pediatrics"
    },
    "General Emergency": {
        "beds": 0.4,
        "icu": 0.2,
        "doctors": 0.2,
        "oxygen": 0.2,
        "specialization": "General"
    }
}

def calculate_score(hospital, weights):
    bed_score = min(hospital['beds_available'] / 20, 1.0)
    icu_score = min(hospital['icu_available'] / 10, 1.0)
    doc_score = min(hospital['doctors_on_duty'] / 10, 1.0)
    oxy_score = min(hospital['oxygen_cylinders'] / 20, 1.0)
    distance_penalty = min(hospital['distance'] / 20, 1.0)
    spec_bonus = 0.2 if weights['specialization'] in hospital['specializations'] else 0
    score = (
        bed_score * weights['beds'] +
        icu_score * weights['icu'] +
        doc_score * weights['doctors'] +
        oxy_score * weights['oxygen'] +
        spec_bonus -
        distance_penalty * 0.1
    )
    return round(score * 100, 1)

def show_ai_recommender(hospitals):

    st.markdown("### 🤖 AI Emergency Recommender")
    st.markdown("Tell us your emergency and we'll find the best hospital instantly")

    st.markdown("""
        <style>
            div[data-baseweb="select"] > div {
                background-color: #ffffff !important;
                color: #212529 !important;
                border-color: #dee2e6 !important;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        emergency_type = st.selectbox(
            "🚨 Select Emergency Type",
            list(EMERGENCY_WEIGHTS.keys()),
            key="emergency_select"
        )

    with col2:
        max_distance = st.slider(
            "📏 Max Distance (km)",
            1, 20, 10,
            key="ai_distance"
        )

    if st.button("🔍 Find Best Hospital", type="primary", use_container_width=True):

        weights = EMERGENCY_WEIGHTS[emergency_type]
        nearby = [h for h in hospitals if h['distance'] <= max_distance]

        if not nearby:
            st.error("No hospitals found within this distance. Try increasing the range.")
            return

        scored = []
        for hospital in nearby:
            score = calculate_score(hospital, weights)
            scored.append({
                **hospital,
                'score': score
            })

        scored = sorted(scored, key=lambda x: x['score'], reverse=True)
        best = scored[0]

        st.markdown("---")
        st.success(f"### ✅ Best Hospital for {emergency_type}")

        c1, c2, c3 = st.columns([2, 1, 1])

        with c1:
            st.markdown(f"## 🏥 {best['name']}")
            st.markdown(f"📍 {best['address']}")
            st.markdown(f"📞 {best['phone']}")
            st.markdown(f"📏 **{best['distance']} km away**")
            st.markdown("**Why recommended:**")
            if weights['specialization'] in best['specializations']:
                st.markdown(f"✅ Has **{weights['specialization']}** specialist")
            st.markdown(f"✅ **{best['beds_available']}** beds available")
            st.markdown(f"✅ **{best['icu_available']}** ICU beds free")
            st.markdown(f"✅ **{best['doctors_on_duty']}** doctors on duty")

        with c2:
            st.metric("🎯 Match Score", f"{best['score']}%")
            st.metric("🛏️ Beds", best['beds_available'])
            st.metric("🏥 ICU", best['icu_available'])

        with c3:
            st.metric("🫁 Oxygen", best['oxygen_cylinders'])
            st.metric("👨‍⚕️ Doctors", best['doctors_on_duty'])
            st.metric("📏 Distance", f"{best['distance']} km")

        st.link_button(
            "🗺️ Get Directions to Best Hospital",
            f"https://www.google.com/maps/dir/?api=1&destination={best['lat']},{best['lon']}",
            use_container_width=True
        )

        st.markdown("---")
        st.markdown("#### 📊 All Hospitals Ranked")

        df_display = pd.DataFrame([{
            "Rank": i+1,
            "Hospital": h['name'],
            "Score": f"{h['score']}%",
            "Beds": h['beds_available'],
            "ICU": h['icu_available'],
            "Oxygen": h['oxygen_cylinders'],
            "Doctors": h['doctors_on_duty'],
            "Distance": f"{h['distance']} km"
        } for i, h in enumerate(scored)])

        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )