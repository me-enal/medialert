import streamlit as st
import json
import os
from data.save_data import save_hospitals
def show_update_panel(hospitals):
    """
    Concept: Forms + Session State — we use a form
    to collect hospital staff input and update the
    data in memory using session state
    """

    st.markdown("### 🔄 Hospital Update Panel")
    st.info("🏥 Hospital staff can update their resource availability here")

    # Concept: Session state for authentication —
    # we store login status so it persists between interactions
    if 'staff_logged_in' not in st.session_state:
        st.session_state['staff_logged_in'] = False

    # Show login form if not logged in
    if not st.session_state['staff_logged_in']:
        st.warning("🔐 Staff login required to update data")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("🔑 Login", use_container_width=True)
            
            if login_btn:
                # Concept: Simple auth check
                # In real app this would check a database
                if username == "admin" and password == "medialert123":
                    st.session_state['staff_logged_in'] = True
                    st.success("✅ Logged in successfully!")
                    st.rerun()
                else:
                    st.error("❌ Wrong username or password")
        return  # Stop here if not logged in

    # Logout button
    if st.button("🚪 Logout"):
        st.session_state['staff_logged_in'] = False
        st.rerun()

    # Concept: selectbox with list comprehension
    # builds dropdown options from hospital data
    hospital_names = [h['name'] for h in hospitals]
    
    selected_name = st.selectbox(
        "Select Your Hospital",
        hospital_names
    )

    # Find selected hospital data
    # Concept: next() with generator — finds first
    # matching item in a list efficiently
    selected = next(
        (h for h in hospitals if h['name'] == selected_name),
        None
    )

    if selected:
        st.markdown(f"**Updating:** {selected['name']}")
        st.markdown("---")

        # Concept: st.form — groups inputs, only
        # processes when submit button is clicked
        with st.form("update_form"):

            col1, col2 = st.columns(2)

            with col1:
                new_beds = st.number_input(
                    "🛏️ Beds Available",
                    min_value=0,
                    max_value=selected['beds_total'],
                    value=selected['beds_available']
                )

                new_icu = st.number_input(
                    "🏥 ICU Beds Available",
                    min_value=0,
                    max_value=selected['icu_total'],
                    value=selected['icu_available']
                )

                new_oxygen = st.number_input(
                    "🫁 Oxygen Cylinders",
                    min_value=0,
                    max_value=100,
                    value=selected['oxygen_cylinders']
                )

            with col2:
                new_doctors = st.number_input(
                    "👨‍⚕️ Doctors on Duty",
                    min_value=0,
                    max_value=50,
                    value=selected['doctors_on_duty']
                )

                new_ventilators = st.number_input(
                    "💨 Ventilators Available",
                    min_value=0,
                    max_value=50,
                    value=selected['ventilators']
                )

                new_24h = st.checkbox(
                    "⏰ Open 24 Hours",
                    value=selected['open_24h']
                )

            # Blood bank update
            st.markdown("**🩸 Update Blood Bank:**")
            blood_cols = st.columns(8)
            blood_types = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
            new_blood = {}

            for i, bt in enumerate(blood_types):
                with blood_cols[i]:
                    new_blood[bt] = st.checkbox(
                        bt,
                        value=selected['blood_bank'].get(bt, False),
                        key=f"update_blood_{bt}"
                    )

            # Concept: form submit button — nothing
            # above runs until this is clicked
            submitted = st.form_submit_button(
                "✅ Update Hospital Data",
                use_container_width=True,
                type="primary"
            )

            if submitted:
                # Concept: updating a dictionary —
                # we find the hospital and change its values
                for hospital in hospitals:
                    if hospital['name'] == selected_name:
                        hospital['beds_available'] = new_beds
                        hospital['icu_available'] = new_icu
                        hospital['oxygen_cylinders'] = new_oxygen
                        hospital['doctors_on_duty'] = new_doctors
                        hospital['ventilators'] = new_ventilators
                        hospital['open_24h'] = new_24h
                        hospital['blood_bank'] = new_blood

                        # Concept: Session state — store
                        # updated data so it persists
                        st.success(f"✅ {selected_name} data updated successfully!")
                        st.session_state['hospitals'] = hospitals

                st.success(f"✅ {selected_name} data updated successfully!")
                st.balloons()