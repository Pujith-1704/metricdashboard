import time
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import matplotlib.pyplot as plt

# Simulated real-time data functions
def get_traffic_data():
    return pd.DataFrame({
        'Time': pd.date_range(start='2024-08-27', periods=10, freq='S'),
        'Traffic Flow': np.random.randint(50, 200, 10)
    })

def get_air_quality_data():
    return pd.DataFrame({
        'Zone': ['North', 'South', 'East', 'West'],
        'AQI': np.random.randint(50, 150, 4)
    })

def get_energy_consumption_data():
    return pd.DataFrame({
        'District': ['A', 'B', 'C', 'D'],
        'Consumption': np.random.randint(1000, 5000, 4)
    })

# Data for Indian states and transport status
state_transport_data = pd.DataFrame({
    'State': ['Maharashtra', 'Tamil Nadu', 'Karnataka', 'Rajasthan'],
    'Latitude': [19.7515, 11.1271, 15.3173, 27.0238],
    'Longitude': [75.7139, 78.6569, 75.7139, 74.2179],
    'Transport_Status': ['easy', 'hard', 'easy', 'hard']
})

# Map transport status to colors
state_transport_data['Color'] = state_transport_data['Transport_Status'].apply(
    lambda status: [0, 255, 0] if status == 'easy' else [255, 0, 0]
)

st.title('City Real-Time Monitoring Dashboard')

# Select metric to display
metric = st.sidebar.selectbox("Select Metric", ["Traffic Flow", "Air Quality", "Energy Consumption", "Public Transport"])

# Placeholder for dynamic content
placeholder = st.empty()

# Real-Time Monitoring Loop
while True:
    if metric == "Traffic Flow":
        data = get_traffic_data()
        with placeholder.container():
            st.write("**Traffic Flow Monitoring**")
            st.line_chart(data.set_index('Time'))
            st.bar_chart(data['Traffic Flow'])

    elif metric == "Air Quality":
        data = get_air_quality_data()
        with placeholder.container():
            st.write("**Air Quality Monitoring**")
            st.bar_chart(data.set_index('Zone'))

    elif metric == "Energy Consumption":
        data = get_energy_consumption_data()
        with placeholder.container():
            st.write("**Energy Consumption Monitoring**")
            
            # Create a pie chart using Matplotlib
            fig, ax = plt.subplots()
            ax.pie(data['Consumption'], labels=data['District'], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Display the pie chart in Streamlit
            st.pyplot(fig)

    elif metric == "Public Transport":
        st.write("**Public Transport Monitoring**")
        
        # Create a Pydeck ScatterplotLayer for states
        layer = pdk.Layer(
            'ScatterplotLayer',
            data=state_transport_data,
            get_position=['Longitude', 'Latitude'],
            get_color='Color',
            get_radius=50000,  # Adjust size of the circles
            pickable=True,
            auto_highlight=True
        )
        
        # Set the viewport location to focus on India
        view_state = pdk.ViewState(
            latitude=20.5937,
            longitude=78.9629,
            zoom=4,
            pitch=0
        )
        
        # Render the map
        r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{State}: {Transport_Status}"})
        st.pydeck_chart(r)

    # Sleep to simulate real-time updates
    time.sleep(5)
