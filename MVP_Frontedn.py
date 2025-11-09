# app.py
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Airbnb Price Predictor (MVP)", page_icon="🏠", layout="wide")

# --- Minimal Styling ---
st.markdown("""
    <style>
      .big-title { font-size: 36px; font-weight: 800; margin-bottom: 0.25rem; }
      .subtitle { color: #6b7280; margin-top: -0.25rem; }
      .card {
        border: 1px solid #e5e7eb; border-radius: 12px; padding: 18px; background: #ffffff;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
      }
      .pill { display:inline-block; padding:2px 8px; border-radius:999px; background:#eef2ff; color:#4338ca; font-size:12px; }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="big-title">Airbnb Price Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Data-driven pricing for optimal profitability · MVP UI preview</div>', unsafe_allow_html=True)
st.divider()

# --- Sidebar: Inputs ---
with st.sidebar:
    st.header("Listing details")
    city = st.selectbox("City", ["Paris", "Vienna", "Berlin", "Zurich"])
    neighborhood = st.text_input("Neighborhood / Arrondissement", placeholder="e.g., Le Marais")
    addr = st.text_input("Street (optional)", placeholder="For your preview only")
    colA, colB = st.columns(2)
    with colA:
        bedrooms = st.number_input("Bedrooms", 0, 10, 1)
        bathrooms = st.number_input("Bathrooms", 0, 10, 1)
        accommodates = st.number_input("Accommodates", 1, 16, 2)
    with colB:
        prop_type = st.selectbox("Property type", ["Entire home/apt", "Private room", "Shared room", "Hotel room"])
        room_quality = st.select_slider("Quality (subjective)", options=list(range(1,6)), value=3)
        min_nights = st.number_input("Minimum nights", 1, 60, 2)

    st.subheader("Amenities")
    amen = st.multiselect(
        "Choose amenities",
        ["Wi-Fi", "Kitchen", "Washer", "Dryer", "Air conditioning", "Heating", "TV", "Elevator", "Parking", "Balcony"],
        default=["Wi-Fi","Kitchen"]
    )
    instant_book = st.toggle("Instant bookable", value=True)
    photos = st.file_uploader("Photos (optional)", accept_multiple_files=True, type=["png","jpg","jpeg"])

    st.subheader("Time window")
    stay_date = st.date_input("Target date", value=date(2025, 6, 15))
    st.caption("Note: This MVP shows a mock prediction for presentation purposes.")

# --- Main content ---
left, right = st.columns([1.1, 1])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Suggested price (mock)")
    # --- Mock calculation for visual impression only ---
    base = 70
    city_factor = {"Paris": 1.35, "Vienna": 1.1, "Berlin": 1.0, "Zurich": 1.8}[city]
    type_factor = {"Entire home/apt": 1.25, "Private room": 0.6, "Shared room": 0.4, "Hotel room": 1.4}[prop_type]
    amen_bonus = min(len(amen) * 3, 30)
    quality_bonus = (room_quality - 3) * 12
    capacity_bonus = max(0, (accommodates - 2) * 6)
    mock_price = int((base + amen_bonus + quality_bonus + capacity_bonus) * city_factor * type_factor)
    low, high = int(mock_price*0.85), int(mock_price*1.15)

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Recommended nightly rate", f"€{mock_price}")
    kpi2.metric("Competitive range", f"€{low} – €{high}")
    kpi3.metric("Occupancy focus", "High", delta="balanced")

    st.markdown("**Rationale (mock):** city factor, property type, capacity, amenities and quality slider.")
    st.progress(min(1.0, (len(amen) + room_quality) / 10))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Feature summary")
    df = pd.DataFrame({
        "Feature": ["City","Neighborhood","Property type","Bedrooms","Bathrooms","Accommodates","Instant book","Amenities count","Min nights"],
        "Value": [city, neighborhood or "-", prop_type, bedrooms, bathrooms, accommodates, "Yes" if instant_book else "No", len(amen), min_nights]
    })
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Map preview")
    # Minimal map seed (Paris center if Paris; else city approx)
    coords = {
        "Paris": (48.8566, 2.3522),
        "Vienna": (48.2082, 16.3738),
        "Berlin": (52.5200, 13.4050),
        "Zurich": (47.3769, 8.5417),
    }[city]
    map_df = pd.DataFrame([{"lat": coords[0], "lon": coords[1]}])
    st.map(map_df, zoom=11)
    st.caption("Map shows a placeholder marker for the selected city.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("What you’ll get in v1")
    st.markdown(
        "- Data ingestion from Inside Airbnb\n"
        "- Model selection (baseline vs. advanced)\n"
        "- Cross-validation & explainability (feature importances)\n"
        "- Neighborhood benchmarks & price bands\n"
        "- Export to PDF/CSV and shareable link"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.divider()
st.markdown('<span class="pill">MVP Preview · No live data</span>', unsafe_allow_html=True)
