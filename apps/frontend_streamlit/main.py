import os

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st


# Environment-aware API URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8666")

# Page config
st.set_page_config(page_title="Weather Time Series", layout="wide")

# Title
st.title("Weather Time Series Dashboard")

# Sidebar for coordinates input
st.sidebar.header("Location Settings")

# Input fields for coordinates
lat = st.sidebar.number_input(
    "Latitude",
    min_value=-90.0,
    max_value=90.0,
    value=40.7128,  # Default to NYC
    step=0.0001,
    format="%.4f",
)

lon = st.sidebar.number_input(
    "Longitude",
    min_value=-180.0,
    max_value=180.0,
    value=-74.0060,  # Default to NYC
    step=0.0001,
    format="%.4f",
)


# Fetch data button
if st.sidebar.button("Fetch Weather Data", type="primary"):
    try:
        # Make API call
        url = f"{API_BASE_URL}/v1/weather/{lat}/{lon}"

        with st.spinner("Fetching weather data..."):
            response = requests.get(url, timeout=10)

        print(response)
        if response.status_code == 200:
            data = response.json()

            # Store in session state
            st.session_state.weather_data = data["data"]
            st.session_state.current_coords = (lat, lon)
            st.success(f"Data fetched successfully for coordinates ({lat}, {lon})")

        else:
            st.error(f"API Error: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        st.error(f"Connection failed. Make sure your FastAPI server is running on {API_BASE_URL}")
    except requests.exceptions.Timeout:
        st.error("Request timeout. API took too long to respond.")
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")


# Display data if available
if "weather_data" in st.session_state:
    coords = st.session_state.current_coords

    # Coordinates label above graph
    st.subheader(f"Weather Data for Coordinates: {coords[0]}, {coords[1]}")

    try:
        # Convert to DataFrame (adjust based on your API response structure)
        df = pd.DataFrame(st.session_state.weather_data)

        # Show data info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            if "timestamp" in df.columns:
                st.metric("Date Range", f"{df.timestamp.nunique()} unique times")
        with col3:
            st.metric("Data Columns", len(df.columns))

        # Plot the time series
        if not df.empty:
            # Detect possible time and value columns (adjust based on your data structure)
            time_cols = [
                col
                for col in df.columns
                if any(word in col.lower() for word in ["time", "date", "timestamp"])
            ]

            numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

            if time_cols and numeric_cols:
                time_col = time_cols[0]

                # Convert timestamp if needed
                if df[time_col].dtype == "object":
                    df[time_col] = pd.to_datetime(df[time_col])

                # Multi-select for which metrics to plot
                selected_metrics = st.multiselect(
                    "Select metrics to display:",
                    numeric_cols,
                    default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols,
                )

                if selected_metrics:
                    # Create plot
                    fig = go.Figure()

                    for metric in selected_metrics:
                        fig.add_trace(
                            go.Scatter(
                                x=df[time_col],
                                y=df[metric],
                                mode="lines+markers",
                                name=metric,
                                line=dict(width=2),
                            )
                        )

                    fig.update_layout(
                        title=f"Weather Time Series - Lat: {coords[0]}, Lon: {coords[1]}",
                        xaxis_title="Time",
                        yaxis_title="Temperatures",
                        hovermode="x unified",
                        height=500,
                    )

                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.warning("Please select at least one metric to display")
            else:
                st.warning("Could not detect time series columns. Showing raw data:")
                st.dataframe(df)

        # Show raw data in expander
        with st.expander("View Raw Data"):
            st.dataframe(df)

        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"weather_data_{coords[0]}_{coords[1]}.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        st.json(st.session_state.weather_data)  # Show raw JSON for debugging

else:
    # Default view when no data loaded
    st.info("👈 Enter coordinates in the sidebar and click 'Fetch Weather Data' to get started")

    # Show example
    st.subheader("Example Usage")
    st.code(
        """
    1. Enter latitude and longitude in the sidebar
    2. Click 'Fetch Weather Data' button
    3. View your time series plot and data

    Default coordinates are set to NYC (40.7128, -74.0060)
    """
    )

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Weather data from FastAPI endpoint")
