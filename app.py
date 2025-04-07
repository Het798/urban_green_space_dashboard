import streamlit as st
import pandas as pd
import plotly.express as px

# Setup
st.set_page_config(page_title="🌳 Urban Green Space Dashboard", layout="wide")
st.title("🌳 Urban Green Space Optimization Dashboard")
st.markdown("Analyze population density vs green area to identify underserved neighborhoods.")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/green_space_data.csv")

df = load_data()

# Sidebar filter
with st.sidebar:
    st.header("🔍 Filter")
    filter_option = st.selectbox(
        "Show neighborhoods where:",
        ["All", "Green Space is Sufficient", "Add Green Space"]
    )

if filter_option == "Add Green Space":
    df_filtered = df[df["Recommendation"] == "Add Green Space"]
elif filter_option == "Green Space is Sufficient":
    df_filtered = df[df["Recommendation"] == "Sufficient"]
else:
    df_filtered = df

# =====================
# 📋 Summary Table
# =====================
st.subheader("📋 Neighborhood Overview")
st.dataframe(df_filtered.style.format({
    "Green_Cover_%": "{:.1f}%",
    "People_per_green_km2": "{:,.0f}"
}))

# =========================
# 📊 Bar Chart
# =========================
st.subheader("📊 People per Green Area by Neighborhood")

fig = px.bar(
    df_filtered.sort_values("People_per_green_km2", ascending=False),
    x="Neighborhood",
    y="People_per_green_km2",
    color="Recommendation",
    title="People per Green Area (Lower is Better)",
    labels={"People_per_green_km2": "People per 1 km² of Green Space"}
)
st.plotly_chart(fig, use_container_width=True)

# =========================
# 🚨 Recommendation Section
# =========================
st.subheader("🚨 Top Underserved Neighborhoods")

critical = df[df["Recommendation"] == "Add Green Space"].sort_values("People_per_green_km2", ascending=False)

if not critical.empty:
    st.error(f"⚠️ {len(critical)} neighborhoods need more green space!")
    st.dataframe(critical[["Neighborhood", "Population", "Green_Cover_%", "People_per_green_km2"]])
else:
    st.success("✅ All neighborhoods meet green space requirements.")

# =========================
# 🗺️ Map: Green Coverage by Neighborhood
# =========================
st.subheader("🗺️ Green Space Coverage Map")

map_fig = px.scatter_mapbox(
    df_filtered,
    lat="Lat",
    lon="Lon",
    size="Green_Cover_%",
    color="Green_Cover_%",
    hover_name="Neighborhood",
    hover_data=["Population", "Green_Area_km2", "Green_Cover_%", "Recommendation"],
    color_continuous_scale="Greens",
    size_max=25,
    zoom=10,
    mapbox_style="carto-positron"
)

st.plotly_chart(map_fig, use_container_width=True)

# ===========================
# 📤 Download Recommendation Data
# ===========================
st.subheader("📁 Export Recommendations")

csv = critical.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Critical Areas as CSV",
    data=csv,
    file_name="green_space_recommendations.csv",
    mime="text/csv"
)
