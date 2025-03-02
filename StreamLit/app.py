import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import random

# ✅ Ensure `st.set_page_config()` is the first Streamlit command
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Load Data from Uploaded File
@st.cache_data
def load_data():
    df = pd.read_csv("https://github.com/rohitshaarma13/Air-Quality-Index-Visualization/blob/main/StreamLit/Air_Quality_Data.csv")
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
    return df

df = load_data()

# Sidebar - Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "Dashboard", "Dataset", "About","Quiz", "Settings","Get In Touch"])

# Dummy Authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username == "Rohit" and password == "Sharma":
            st.session_state.logged_in = True
            st.sidebar.success("Logged in successfully!")
        else:
            st.sidebar.error("Invalid credentials!")

if st.session_state.logged_in:
    if menu == "Home":
       st.title("🌍 Welcome to the Air Quality Dashboard")
       st.write("This dashboard helps visualize air quality data across different cities.")
       st.write("Use the navigation panel to explore the dataset, view visualizations, and analyze trends.")
    
       st.write("### Why Monitor Air Quality?")
       st.write(
        "Air pollution is a major environmental risk to public health. Monitoring air quality "
        "helps in identifying pollution sources, assessing health risks, and taking corrective measures "
        "to improve air conditions. Through this dashboard, users can gain insights into various air quality "
        "parameters, including AQI, PM2.5, PM10, temperature, and humidity."
    )
       st.write("### How This Dashboard Works")
       st.write(
        "1. **Dataset Section** - Explore the raw air quality data collected over time.\n"
        "2. **Dashboard Section** - View interactive charts and Power BI integration for deeper analysis.\n"
        "3. **Filters & Trends** - Customize filters to analyze specific cities, AQI categories, and time periods.\n"
        "4. **Settings & Customization** - Adjust theme settings to personalize your experience."
    )

       st.write("Start exploring the air quality trends and make data-driven decisions!")

    elif menu == "Dashboard":
        st.title("📊 Air Quality Dashboard")
        
        # Filters Section
        st.subheader("Filters")
        col1, col2, col3 = st.columns(3)
        with col1:
            date_range = st.date_input("Select Date Range", [])
        with col2:
            category = st.selectbox("Select Category", ["All"] + list(df['AQI Category'].dropna().unique()))
        with col3:
            city = st.selectbox("Select City", ["All"] + list(df['City'].dropna().unique()))
        
        # Apply Filters
        filtered_df = df.copy()
        if date_range:
            start_date = pd.to_datetime(date_range[0])
            end_date = pd.to_datetime(date_range[-1]) if len(date_range) > 1 else start_date
            filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]
        if category != "All":
            filtered_df = filtered_df[filtered_df['AQI Category'] == category]
        if city != "All":
            filtered_df = filtered_df[filtered_df['City'] == city]

        if filtered_df.empty:
            st.warning("No data available for the selected filters.")
        else:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Average AQI", round(filtered_df['AQI'].mean(), 2))
            col2.metric("Average PM2.5", round(filtered_df['PM2.5'].mean(), 2))
            col3.metric("Average PM10", round(filtered_df['PM10'].mean(), 2))
            col4.metric("PM2.5/PM10 Ratio", round(filtered_df['PM2.5/PM10 Ratio'].mean(), 2))

            # Power BI Dashboard Integration
            st.subheader("📊 Power BI Dashboard")
            power_bi_url = "https://app.powerbi.com/view?r=eyJrIjoiZmI5ZmE4ZDctNmJiOC00MjhhLWI2N2YtYWVhOTFhYzc1ZTljIiwidCI6ImYzN2Q3OTFlLWRkMDctNDZjYS1iYzI5LTUwNzIzNTgwMWVmMyJ9"
            with st.expander("View Power BI Dashboard"):
                st.components.v1.iframe(power_bi_url, width=1200, height=700, scrolling=True)

            # Charts Section
        st.subheader("Visualizations")

        # AQI Trend Over Time
        fig_trend = px.line(filtered_df, x='Date', y='AQI', color='City', title='AQI Trend Over Time')
        st.plotly_chart(fig_trend, use_container_width=True)

        # AQI Category Distribution
        fig_pie = px.pie(filtered_df, names='AQI Category', title='AQI Category Distribution')
        st.plotly_chart(fig_pie, use_container_width=True)

        # Top & Least Polluted Cities
        top_cities = filtered_df.groupby('City')['AQI'].mean().nlargest(3).reset_index()
        least_cities = filtered_df.groupby('City')['AQI'].mean().nsmallest(3).reset_index()

        col1, col2 = st.columns(2)
        fig_top = px.bar(top_cities, x='City', y='AQI', title='Top 3 Polluted Cities', color='City')
        fig_least = px.bar(least_cities, x='City', y='AQI', title='Least Polluted Cities', color='City')
        col1.plotly_chart(fig_top, use_container_width=True)
        col2.plotly_chart(fig_least, use_container_width=True)

        # Additional Charts
        fig_scatter = px.scatter(filtered_df, x='Temperature', y='Humidity', size='AQI', color='City', title='Temperature & Humidity vs AQI')
        st.plotly_chart(fig_scatter, use_container_width=True)

        fig_box = px.box(filtered_df, x='City', y='AQI', title='AQI Distribution by City')
        st.plotly_chart(fig_box, use_container_width=True)

        fig_hist = px.histogram(filtered_df, x='AQI', title='AQI Frequency Distribution', nbins=30)
        st.plotly_chart(fig_hist, use_container_width=True)

        fig_heatmap = px.density_heatmap(filtered_df, x='Temperature', y='AQI', title='Temperature vs AQI Density')
        st.plotly_chart(fig_heatmap, use_container_width=True)

        fig_violin = px.violin(filtered_df, x='City', y='PM2.5', title='PM2.5 Distribution by City', box=True, points='all')
        st.plotly_chart(fig_violin, use_container_width=True)

        fig_facet = px.scatter(filtered_df, x='Temperature', y='AQI', color='City', facet_col='AQI Category', title='AQI vs Temperature by Category')
        st.plotly_chart(fig_facet, use_container_width=True)


    elif menu == "Dataset":
        st.title("📄 Dataset Overview")
        st.write("Here is a preview of the dataset used for visualization.")
        st.dataframe(df.head(10))

        st.write("### Dataset Statistics")
        st.write(df.describe())

        st.write("### 📌 Understanding the Dataset")
        st.write(
        "The dataset contains air quality data collected from different cities. Each row represents a recorded air quality measurement "
        "with various attributes such as AQI, particulate matter levels, temperature, and humidity."
    )

        st.write("### 🔍 Column Descriptions")
        st.markdown("""
    - **Date**: The date when the air quality data was recorded (Format: `dd-mm-yyyy`).
    - **City**: The name of the city where the measurements were taken.
    - **AQI (Air Quality Index)**: A numerical value indicating the level of air pollution.
    - **AQI Category**: Classification of AQI (e.g., Good, Moderate, Unhealthy).
    - **PM2.5**: Fine particulate matter (≤2.5 µm) concentration (µg/m³).
    - **PM10**: Coarse particulate matter (≤10 µm) concentration (µg/m³).
    - **PM2.5/PM10 Ratio**: Ratio indicating the proportion of fine particles in total particulate matter.
    - **Temperature**: The ambient air temperature (°C).
    - **Humidity**: The relative humidity (%) in the air at the time of measurement.
    """)

        st.write("### 📊 AQI Categories & Health Impact")
        st.markdown("""
    | **AQI Value** | **Category**                   | **Health Impact** |
    |--------------|-----------------------------|-----------------|
    | 0 - 50      | Good                        | Minimal or no risk. |
    | 51 - 100    | Moderate                    | Acceptable air quality, but some pollutants may be concerning for sensitive individuals. |
    | 101 - 150   | Unhealthy for Sensitive Groups | Health effects for children, elderly, and people with respiratory conditions. |
    | 151 - 200   | Unhealthy                    | Everyone may begin to experience health effects. |
    | 201 - 300   | Very Unhealthy               | Health warnings issued; significant risks for all people. |
    | 301 - 500   | Hazardous                    | Emergency conditions; serious health effects for the entire population. |
    """)

        st.write("### 📈 How Are the Values Calculated?")
        st.markdown("""
    - **AQI Calculation**: The AQI is computed based on pollutant concentrations using a standard formula. The highest individual pollutant concentration determines the AQI.
    - **PM2.5 and PM10 Measurement**: These values are obtained using air quality monitoring stations equipped with laser-based sensors.
    - **Temperature & Humidity**: Collected from meteorological sensors to analyze their impact on pollution levels.
    """)

        st.write("### 🌍 Why Is This Data Important?")
        st.markdown("""
    - **Environmental Monitoring**: Helps in tracking pollution trends.
    - **Health Analysis**: High AQI values indicate potential respiratory and cardiovascular risks.
    - **Urban Planning**: Enables authorities to implement policies to reduce pollution in critical areas.
    """)

    
    elif menu == "About":
        st.title("ℹ️ About This Project")

        st.write(
        "This project is designed to provide insights into air quality across various cities using interactive visualizations. "
        "By analyzing data on pollutants, meteorological conditions, and AQI trends, users can better understand environmental conditions "
        "and their impact on health and daily life."
    )

        st.write("### 🌍 Why Air Quality Monitoring Matters")
        st.markdown("""
    - **Public Health**: Poor air quality is linked to respiratory diseases, cardiovascular problems, and other health issues.
    - **Climate Impact**: Air pollutants contribute to climate change by affecting atmospheric composition.
    - **Urban Planning**: Helps governments and policymakers implement strategies to reduce pollution in critical areas.
    - **Awareness & Action**: Individuals can take necessary precautions based on real-time air quality data.
    """)

        st.write("### 📊 Key Features of This Dashboard")
        st.markdown("""
    - **📌 Dataset Exploration**: Users can view and analyze raw air quality data.
    - **📈 Visual Analytics**: Interactive charts for AQI trends, pollutant distribution, and city-wise analysis.
    - **🔍 Filtered Insights**: Custom filters to explore specific cities, AQI levels, and time periods.
    - **📊 Power BI Integration**: Advanced data visualization with external reports.
    - **⚙️ Settings & Customization**: Options to personalize the dashboard experience.
    """)

        st.write("### 📜 Data Source & Collection")
        st.markdown("""
    - The data is sourced from various air quality monitoring stations and compiled into a structured dataset.
    - **Pollutants Measured**: PM2.5, PM10, AQI, Temperature, Humidity.
    - **Data Format**: CSV file containing historical records of air quality across different cities.
    """)

        st.write("### 📌 Future Improvements")
        st.markdown("""
    - **🚀 Real-Time Data Integration**: Incorporating live air quality APIs for real-time updates.
    - **🧠 AI-Based Predictions**: Machine learning models to forecast air quality trends.
    - **📍 Geospatial Mapping**: Interactive maps to visualize pollution levels across different regions.
    """)

        st.success("This dashboard is a step towards raising awareness and encouraging action for cleaner air! 🌱")
    elif menu == "Quiz":
        st.title("Air Quality Quiz")

    # Store quiz score in session state
        if "score" not in st.session_state:
            st.session_state.score = 0
        if "answered_questions" not in st.session_state:
            st.session_state.answered_questions = set()

        quiz_questions = [
           {"question": "Which pollutant is the primary contributor to the formation of acid rain?",
            "options": ["Carbon Monoxide (CO)", "Sulfur Dioxide (SO₂)", "Ozone (O₃)", "Lead (Pb)"],
            "answer": "Sulfur Dioxide (SO₂)"},
           {"question": "What is the full form of PM2.5 in air quality measurements?",
            "options": ["Particulate Matter less than 2.5 millimeters", "Particulate Material of 2.5 density",
            "Particulate Matter smaller than 2.5 micrometers", "Pollution Mass at 2.5 meters"],
            "answer": "Particulate Matter smaller than 2.5 micrometers"},
           {"question": "Which of the following gases has the highest Global Warming Potential (GWP) over 100 years?",
            "options": ["Carbon Dioxide (CO₂)", "Methane (CH₄)", "Nitrous Oxide (N₂O)", "Sulfur Hexafluoride (SF₆)"],
            "answer": "Sulfur Hexafluoride (SF₆)"},
           {"question": "What is the primary reason that ground-level ozone (O₃) is harmful to human health?",
            "options": ["It directly causes global warming", "It reacts with lung tissues and causes respiratory issues",
            "It blocks UV radiation, reducing Vitamin D synthesis", "It enhances oxygen levels in polluted areas"],
            "answer": "It reacts with lung tissues and causes respiratory issues"},
           {"question": "Which air pollutant is responsible for smog formation in urban areas?",
            "options": ["Carbon Monoxide (CO)", "Particulate Matter (PM10)", "Nitrogen Oxides (NOₓ)", "Ozone (O₃)"],
            "answer": "Nitrogen Oxides (NOₓ)"},
           {"question": "What is the major source of Volatile Organic Compounds (VOCs) in urban environments?",
            "options": ["Vehicle emissions and industrial processes", "Agricultural crop burning", "Forest wildfires", "Indoor cooking activities"],
            "answer": "Vehicle emissions and industrial processes"},
           {"question": "What is the main reason AQI values are generally worse in winter?",
            "options": ["Higher temperature increases pollutant reaction rates", "Air inversion traps pollutants near the surface",
            "Increased levels of ultraviolet (UV) radiation", "Trees absorb fewer pollutants during winter"],
            "answer": "Air inversion traps pollutants near the surface"},
           {"question": "Which of the following air pollutants is NOT a direct greenhouse gas?",
            "options": ["Carbon Dioxide (CO₂)", "Methane (CH₄)", "Nitrogen Oxides (NOₓ)", "Sulfur Hexafluoride (SF₆)"],
            "answer": "Nitrogen Oxides (NOₓ)"},
           {"question": "What is the primary cause of indoor air pollution in developing countries?",
            "options": ["Poor ventilation in high-rise buildings", "Burning biomass fuels (wood, charcoal, cow dung)",
            "Air conditioning and refrigeration leaks", "Electronic waste emissions"],
            "answer": "Burning biomass fuels (wood, charcoal, cow dung)"},
           {"question": "Which air pollutant is known to have the strongest link to lung cancer?",
            "options": ["Ozone (O₃)", "PM2.5", "Nitrogen Dioxide (NO₂)", "Carbon Monoxide (CO)"],
            "answer": "PM2.5"},
           ]

        for i, q in enumerate(quiz_questions):
            st.subheader(f"Question {i+1}: {q['question']}")
            choice = st.radio("Select your answer:", q['options'], key=f"q{i}")

            if st.button(f"Submit Answer {i+1}", key=f"btn{i}"):
              if i not in st.session_state.answered_questions:
                st.session_state.answered_questions.add(i)  # Mark question as answered
                if choice == q['answer']:
                    st.session_state.score += 1
                    st.success("Correct! ✅")
                else:
                    st.error(f"Wrong! ❌ The correct answer is {q['answer']}")

        st.write("### Final Score: ", st.session_state.score, f"/ {len(quiz_questions)}")

        if st.button("Restart Quiz"):
           st.session_state.score = 0
           st.session_state.answered_questions = set()
           st.rerun()


    elif menu == "Settings":
        st.title("⚙️ Settings")
        theme = st.radio("Choose Theme", ["Light", "Dark"])
        if theme == "Dark":
            st.markdown("<style>body { background-color: black; color: white; }</style>", unsafe_allow_html=True)
        st.success("Settings Saved!")
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    # Contact Form with CSS Styling
    elif menu == "Get In Touch":
        st.title("📞 Get In Touch")

        contact_form = """
    <style>
        .contact-form input, .contact-form textarea {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        .contact-form button {
            width: 100%;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .contact-form button:hover {
            background-color: #45a049;
        }
    </style>
    <form class="contact-form" action="https://formsubmit.co/sharmarohits814@gmail.com" method="POST">
        <input type="text" name="name" placeholder="Your Name" required>
        <input type="email" name="email" placeholder="Your Email" required>
        <textarea name="message" placeholder="Your Message" rows="4" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
        st.markdown(contact_form, unsafe_allow_html=True)

    # Footer
        st.write("---")
        st.write("Thanks for visiting! Feel free to connect with me.")

else:
    st.warning("Please log in to access the dashboard.")
    
