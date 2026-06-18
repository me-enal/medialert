import folium
from streamlit_folium import st_folium
import streamlit as st

def show_map(hospitals):
    """
    Concept: Folium Map — we create a map centered
    on Ludhiana and add a marker for each hospital
    """

    # Concept: Map center — latitude/longitude of Ludhiana
    map_center = [30.9010, 75.8573]

    # Create the base map
    # Concept: zoom_start — higher = more zoomed in
    m = folium.Map(
        location=map_center,
        zoom_start=12,
        tiles="OpenStreetMap"
    )

    # Concept: Loop — add one marker per hospital
    for hospital in hospitals:

        # Color based on bed availability
        # Concept: Conditional expression (ternary)
        if hospital['beds_available'] == 0:
            color = "red"
        elif hospital['beds_available'] <= 3:
            color = "orange"
        else:
            color = "green"

        # Concept: HTML popup — custom styled info
        # window that appears when you click a pin
        popup_html = f"""
        <div style="font-family:Arial; width:220px">
            <h4 style="color:#c0392b;margin:0">🏥 {hospital['name']}</h4>
            <hr style="margin:5px 0">
            <b>🛏️ Beds:</b> {hospital['beds_available']} free<br>
            <b>🏥 ICU:</b> {hospital['icu_available']} free<br>
            <b>🫁 Oxygen:</b> {hospital['oxygen_cylinders']} cylinders<br>
            <b>👨‍⚕️ Doctors:</b> {hospital['doctors_on_duty']} on duty<br>
            <b>📞</b> {hospital['phone']}<br>
            <hr style="margin:5px 0">
            <a href="https://www.google.com/maps/dir/?api=1&destination={hospital['lat']},{hospital['lon']}"
               target="_blank"
               style="background:#c0392b;color:white;padding:4px 10px;
                      border-radius:4px;text-decoration:none;font-size:12px">
               🗺️ Get Directions
            </a>
        </div>
        """

        # Add marker to map
        # Concept: folium.Marker — a pin on the map
        folium.Marker(
            location=[hospital['lat'], hospital['lon']],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"🏥 {hospital['name']} — {hospital['beds_available']} beds",
            icon=folium.Icon(color=color, icon="plus-sign", prefix="glyphicon")
        ).add_to(m)

    # Concept: st_folium — renders the folium map
    # inside Streamlit and returns interaction data
    st_folium(m, width=None, height=500)