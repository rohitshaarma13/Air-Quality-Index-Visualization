import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ Ensure `st.set_page_config()` is the first Streamlit command
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Dark theme styling
st.markdown(
    """
    <style>
    body {
        background-color: #1E1E1E;
        color: white;
    }
    .stTextInput, .stSelectbox, .stDateInput {
        background-color: #333333 !important;
        color: white !important;
    }
    .stButton>button {
        background-color: #FF4B4B !important;
        color: white !important;
    }
    iframe {
        border-radius: 10px;
    }
    .dashboard-title {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        background-color: black;
        padding: 10px;
        border-radius: 10px;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar - Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Dashboard", "Settings"])

# Dummy Authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username == "admin" and password == "password":
            st.session_state.logged_in = True
            st.sidebar.success("Logged in successfully!")
        else:
            st.sidebar.error("Invalid credentials!")

if st.session_state.logged_in:
    if menu == "Dashboard":
        # Title with dark theme styling
        st.markdown('<div class="dashboard-title">AIR QUALITY INDEX VISUALIZATION</div>', unsafe_allow_html=True)

        # Load Data
        df = pd.read_csv("d:\\Air Quality Data\\Air_Quality_Data.csv")
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

        # Filters Section
        st.subheader("Filters")
        col1, col2, col3 = st.columns(3)

        with col1:
            date_range = st.date_input("Select Date Range", [])
        with col2:
            category = st.selectbox("Select Category", ["All"] + list(df['AQI Category'].unique()))
        with col3:
            city = st.selectbox("Select City", ["All"] + list(df['City'].unique()))

        # Apply Filters
        if date_range:
            df = df[(df['Date'] >= pd.to_datetime(date_range[0])) & (df['Date'] <= pd.to_datetime(date_range[1]))]
        if category != "All":
            df = df[df['AQI Category'] == category]
        if city != "All":
            df = df[df['City'] == city]

        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Average AQI", round(df['AQI'].mean(), 2))
        col2.metric("Average PM2.5", round(df['PM2.5'].mean(), 2))
        col3.metric("Average PM10", round(df['PM10'].mean(), 2))
        col4.metric("PM2.5/PM10 Ratio", round(df['PM2.5/PM10 Ratio'].mean(), 2))

        # Charts Section
        st.subheader("Visualizations")

        # AQI Trend Over Time
        fig_trend = px.line(df, x='Date', y='AQI', color='City', title='AQI Trend Over Time')
        st.plotly_chart(fig_trend, use_container_width=True)

        # AQI Category Distribution
        fig_pie = px.pie(df, names='AQI Category', title='AQI Category Distribution')
        st.plotly_chart(fig_pie, use_container_width=True)

        # Top & Least Polluted Cities
        top_cities = df.groupby('City')['AQI'].mean().nlargest(3).reset_index()
        least_cities = df.groupby('City')['AQI'].mean().nsmallest(3).reset_index()

        col1, col2 = st.columns(2)
        fig_top = px.bar(top_cities, x='City', y='AQI', title='Top 3 Polluted Cities', color='City')
        fig_least = px.bar(least_cities, x='City', y='AQI', title='Least Polluted Cities', color='City')
        col1.plotly_chart(fig_top, use_container_width=True)
        col2.plotly_chart(fig_least, use_container_width=True)

        # Additional Charts
        fig_scatter = px.scatter(df, x='Temperature', y='Humidity', size='AQI', color='City', title='Temperature & Humidity vs AQI')
        st.plotly_chart(fig_scatter, use_container_width=True)

        fig_box = px.box(df, x='City', y='AQI', title='AQI Distribution by City')
        st.plotly_chart(fig_box, use_container_width=True)

        fig_hist = px.histogram(df, x='AQI', title='AQI Frequency Distribution', nbins=30)
        st.plotly_chart(fig_hist, use_container_width=True)

        fig_heatmap = px.density_heatmap(df, x='Temperature', y='AQI', title='Temperature vs AQI Density')
        st.plotly_chart(fig_heatmap, use_container_width=True)

        fig_violin = px.violin(df, x='City', y='PM2.5', title='PM2.5 Distribution by City', box=True, points='all')
        st.plotly_chart(fig_violin, use_container_width=True)

        fig_facet = px.scatter(df, x='Temperature', y='AQI', color='City', facet_col='AQI Category', title='AQI vs Temperature by Category')
        st.plotly_chart(fig_facet, use_container_width=True)

    elif menu == "Settings":
        st.title("⚙️ Settings")
        theme = st.radio("Choose Theme", ["Light", "Dark"])
        if theme == "Dark":
            st.markdown("<style>body { background-color: black; color: white; }</style>", unsafe_allow_html=True)
        st.success("Settings Saved!")

        # Logout Button
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun()

else:
    st.warning("Please log in to access the dashboard.")
