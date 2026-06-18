import streamlit as st

def get_status_color(value, warning_threshold, danger_threshold):
    if value <= danger_threshold:
        return "🔴"
    elif value <= warning_threshold:
        return "🟡"
    else:
        return "🟢"

def show_hospital_card(hospital):

    bed_color = '#2ecc71' if hospital['beds_available'] > 5 else '#f39c12' if hospital['beds_available'] > 0 else '#e74c3c'
    icu_color = '#2ecc71' if hospital['icu_available'] > 3 else '#f39c12' if hospital['icu_available'] > 0 else '#e74c3c'
    oxy_color = '#2ecc71' if hospital['oxygen_cylinders'] > 5 else '#f39c12' if hospital['oxygen_cylinders'] > 0 else '#e74c3c'
    doc_color = '#2ecc71' if hospital['doctors_on_duty'] > 2 else '#f39c12' if hospital['doctors_on_duty'] > 0 else '#e74c3c'
    border_color = '#2ecc71' if hospital['beds_available'] > 5 else '#f39c12' if hospital['beds_available'] > 0 else '#e74c3c'

    type_bg = '#d4edda' if hospital['type'] == 'Government' else '#d1ecf1'
    type_color = '#155724' if hospital['type'] == 'Government' else '#0c5460'
    type_label = '🏛️ Government' if hospital['type'] == 'Government' else '🏢 Private'

    open_bg = '#d4edda' if hospital['open_24h'] else '#fff3cd'
    open_color = '#155724' if hospital['open_24h'] else '#856404'
    open_label = '✅ Open 24h' if hospital['open_24h'] else '⏰ Limited Hours'

    specs_html = ''.join([
        f'<span style="background:#e9ecef;color:#495057;padding:3px 10px;border-radius:12px;font-size:11px;margin-right:4px">{s}</span>'
        for s in hospital['specializations']
    ])

    html = f"""
    <div style="background:#ffffff;border:1px solid #e9ecef;border-left:5px solid {border_color};border-radius:10px;padding:20px 24px;margin-bottom:8px;box-shadow:0 2px 8px rgba(0,0,0,0.06)">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px">
            <div>
                <h3 style="margin:0;color:#212529;font-size:20px;font-weight:600">🏥 {hospital['name']}</h3>
                <p style="margin:4px 0 0 0;color:#6c757d;font-size:13px">📍 {hospital['address']}</p>
                <p style="margin:2px 0 0 0;color:#6c757d;font-size:13px">📞 {hospital['phone']}</p>
            </div>
            <div style="text-align:right">
                <span style="background:{type_bg};color:{type_color};padding:4px 12px;border-radius:20px;font-size:12px;font-weight:500;display:inline-block;margin-bottom:6px">{type_label}</span>
                <br/>
                <span style="background:{open_bg};color:{open_color};padding:4px 12px;border-radius:20px;font-size:12px;font-weight:500;display:inline-block;margin-bottom:6px">{open_label}</span>
                <br/>
                <span style="color:#6c757d;font-size:13px">📏 {hospital['distance']} km away</span>
            </div>
        </div>
        <hr style="border:none;border-top:1px solid #e9ecef;margin:12px 0"/>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:14px">
            <div style="background:#f8f9fa;border-radius:8px;padding:12px;text-align:center;border:1px solid #e9ecef">
                <div style="font-size:22px;font-weight:700;color:{bed_color}">{hospital['beds_available']}</div>
                <div style="font-size:11px;color:#6c757d;margin-top:2px">🛏️ Beds Free</div>
                <div style="font-size:10px;color:#adb5bd">of {hospital['beds_total']} total</div>
            </div>
            <div style="background:#f8f9fa;border-radius:8px;padding:12px;text-align:center;border:1px solid #e9ecef">
                <div style="font-size:22px;font-weight:700;color:{icu_color}">{hospital['icu_available']}</div>
                <div style="font-size:11px;color:#6c757d;margin-top:2px">🏥 ICU Beds</div>
                <div style="font-size:10px;color:#adb5bd">of {hospital['icu_total']} total</div>
            </div>
            <div style="background:#f8f9fa;border-radius:8px;padding:12px;text-align:center;border:1px solid #e9ecef">
                <div style="font-size:22px;font-weight:700;color:{oxy_color}">{hospital['oxygen_cylinders']}</div>
                <div style="font-size:11px;color:#6c757d;margin-top:2px">🫁 O₂ Cylinders</div>
                <div style="font-size:10px;color:#adb5bd">available</div>
            </div>
            <div style="background:#f8f9fa;border-radius:8px;padding:12px;text-align:center;border:1px solid #e9ecef">
                <div style="font-size:22px;font-weight:700;color:{doc_color}">{hospital['doctors_on_duty']}</div>
                <div style="font-size:11px;color:#6c757d;margin-top:2px">👨‍⚕️ Doctors</div>
                <div style="font-size:10px;color:#adb5bd">on duty</div>
            </div>
        </div>
        <div style="margin-bottom:14px">
            <span style="font-size:12px;color:#6c757d;font-weight:500">Specializations: </span>
            {specs_html}
        </div>
        <hr style="border:none;border-top:1px solid #e9ecef;margin:12px 0"/>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

    with st.expander("🩸 View Blood Bank Availability"):
        blood_cols = st.columns(8)
        for i, (blood_type, available) in enumerate(hospital['blood_bank'].items()):
            with blood_cols[i]:
                if available:
                    st.success(blood_type)
                else:
                    st.error(blood_type)

    btn1, btn2, btn3 = st.columns(3)
    with btn1:
        st.link_button(
            "🗺️ Get Directions",
            f"https://www.google.com/maps/dir/?api=1&destination={hospital['lat']},{hospital['lon']}",
            use_container_width=True
        )
    with btn2:
        st.link_button(
            "📞 Call Hospital",
            f"tel:{hospital['phone']}",
            use_container_width=True
        )
    with btn3:
        if st.button("ℹ️ More Details", key=f"details_{hospital['id']}", use_container_width=True):
            st.session_state['selected_hospital'] = hospital['id']

    st.markdown("<div style='margin-bottom:20px'></div>", unsafe_allow_html=True)