import streamlit as st
import pandas as pd

def show_stats(hospitals):
    """
    Concept: Pandas — converting a list of dictionaries
    into a DataFrame lets us do math on columns easily
    """

    # Concept: pd.DataFrame — creates a table from list of dicts
    df = pd.DataFrame(hospitals)

    st.markdown("### 📊 Live Resource Summary")

    # Concept: st.columns — 5 equal columns side by side
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        total_beds = int(df['beds_available'].sum())
        st.metric(
            label="🛏️ Total Beds Free",
            value=total_beds,
            delta="across all hospitals"
        )

    with c2:
        total_icu = int(df['icu_available'].sum())
        st.metric(
            label="🏥 ICU Beds Free",
            value=total_icu,
            delta="across all hospitals"
        )

    with c3:
        total_oxygen = int(df['oxygen_cylinders'].sum())
        st.metric(
            label="🫁 Oxygen Cylinders",
            value=total_oxygen,
            delta="across all hospitals"
        )

    with c4:
        total_doctors = int(df['doctors_on_duty'].sum())
        st.metric(
            label="👨‍⚕️ Doctors On Duty",
            value=total_doctors,
            delta="across all hospitals"
        )

    with c5:
        total_hospitals = len(hospitals)
        open_24h = len([h for h in hospitals if h['open_24h']])
        st.metric(
            label="🏥 Hospitals",
            value=total_hospitals,
            delta=f"{open_24h} open 24h"
        )

    st.markdown("---")