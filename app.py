
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Public Transport Analytics",
    page_icon="🚌",
    layout="wide"
)

st.title("🚌 Public Transport Passenger Analytics")
st.write("Analyze bus passenger data using Python.")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/cta_ridership.csv")

    df.columns = df.columns.str.lower().str.strip()

    df["date"] = pd.to_datetime(df["date"])
    df["rides"] = pd.to_numeric(df["rides"])

    df = df.dropna(subset=["date", "route", "rides"])

    return df

try:
    df = load_data()

    # Sidebar
    st.sidebar.header("Dashboard Filters")

    routes = sorted(df["route"].astype(str).unique())

    selected_route = st.sidebar.selectbox(
        "Select Bus Route",
        routes
    )

    # Statistics
    total_passengers = df["rides"].sum()
    total_routes = df["route"].nunique()
    average_passengers = df["rides"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Passenger Rides",
        f"{total_passengers:,.0f}"
    )

    col2.metric(
        "Total Bus Routes",
        total_routes
    )

    col3.metric(
        "Average Passengers",
        f"{average_passengers:,.0f}"
    )

    # Route analysis
    st.header("Route Passenger Analysis")

    route_data = df[
        df["route"].astype(str) == selected_route
    ]

    route_data = route_data.sort_values("date")

    fig1 = px.line(
        route_data.tail(180),
        x="date",
        y="rides",
        title="Daily Passenger Trend"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # Top routes
    st.header("Top 10 Busy Bus Routes")

    top_routes = (
        df.groupby("route")["rides"]
        .sum()
        .nlargest(10)
        .reset_index()
    )

    fig2 = px.bar(
        top_routes,
        x="route",
        y="rides",
        title="Passenger Count by Route"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # Day type analysis
    st.header("Passenger Day-Type Analysis")

    day_analysis = (
        df.groupby("daytype")["rides"]
        .mean()
        .reset_index()
    )

    fig3 = px.bar(
        day_analysis,
        x="daytype",
        y="rides",
        title="Average Passenger Rides by Day Type"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # Dataset display
    st.header("Passenger Dataset")

    st.dataframe(
        df.tail(100),
        use_container_width=True
    )

    st.success("Dashboard loaded successfully!")

except Exception as e:
    st.error(f"Error loading dashboard: {e}")

st.caption("Public Transport Passenger Analytics Mini Project")
