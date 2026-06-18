import streamlit as st

# Concept: Function — takes one hospital dictionary and displays it as a card
def get_status_color(value, warning_threshold, danger_threshold):
    """
    Concept: Conditional logic — returns a color based on how critical the value is
    green = safe, orange = warning, red = danger
    """
    if value <= danger_threshold:
        return "🔴"
    elif value <= warning_threshold:
        return "🟡"
    else:
        return "🟢"

def show_hospital_card(hospital):
    """
    Concept: Streamlit components — st.container, st.columns, st.metric 
    are built-in UI building blocks
    """
    
    # Concept: st.container — groups everything inside one visual block
    with st.container():
        
        # Hospital name and basic info
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### 🏥 {hospital['name']}")
            st.markdown(f"📍 {hospital['address']}")
            st.markdown(f"📞 {hospital['phone']}")
        
        with col2:
            # Hospital type badge
            if hospital['type'] == "Government":
                st.success("🏛️ Govt")
            else:
                st.info("🏢 Private")
            
            # 24h badge
            if hospital['open_24h']:
                st.success("✅ 24h Open")
            else:
                st.warning("⏰ Limited hrs")
            
            st.markdown(f"📏 **{hospital['distance']} km away**")
        
        st.divider()
        
        # Concept: st.columns — splits the screen into equal parts side by side
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            bed_icon = get_status_color(hospital['beds_available'], 10, 3)
            st.metric(
                label=f"{bed_icon} Beds Free",
                value=hospital['beds_available'],
                delta=f"of {hospital['beds_total']} total"
            )
        
        with c2:
            icu_icon = get_status_color(hospital['icu_available'], 5, 1)
            st.metric(
                label=f"{icu_icon} ICU Beds",
                value=hospital['icu_available'],
                delta=f"of {hospital['icu_total']} total"
            )
        
        with c3:
            oxy_icon = get_status_color(hospital['oxygen_cylinders'], 5, 2)
            st.metric(
                label=f"{oxy_icon} O₂ Cylinders",
                value=hospital['oxygen_cylinders'],
                delta="cylinders"
            )
        
        with c4:
            doc_icon = get_status_color(hospital['doctors_on_duty'], 3, 1)
            st.metric(
                label=f"{doc_icon} Doctors",
                value=hospital['doctors_on_duty'],
                delta="on duty"
            )
        
        # Specializations
        st.markdown("**Specializations:**")
        # Concept: List comprehension — builds a string from a list in one line
        specs = " • ".join([f"`{s}`" for s in hospital['specializations']])
        st.markdown(specs)
        
        # Blood bank section
        with st.expander("🩸 Blood Bank Availability"):
            # Concept: Dictionary iteration — loop through key-value pairs
            blood_cols = st.columns(8)
            for i, (blood_type, available) in enumerate(hospital['blood_bank'].items()):
                with blood_cols[i]:
                    if available:
                        st.success(blood_type)
                    else:
                        st.error(blood_type)
        
        # Action buttons
        btn1, btn2, btn3 = st.columns(3)
        with btn1:
            st.link_button(
                "🗺️ Get Directions",
                f"https://www.google.com/maps/dir/?api=1&destination={hospital['lat']},{hospital['lon']}"
            )
        with btn2:
            st.link_button(
                "📞 Call Hospital",
                f"tel:{hospital['phone']}"
            )
        with btn3:
            # Concept: Session state — remembers which hospital was selected
            if st.button(f"ℹ️ More Details", key=f"details_{hospital['id']}"):
                st.session_state['selected_hospital'] = hospital['id']
        
        # Visual separator between cards
        st.markdown("---")