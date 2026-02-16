import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Flight Price Predictor",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .prediction-price {
        font-size: 3.5rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .feature-card {
        background-color: #f8f9fa;
        color: #424242;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #1E88E5;
    }
    .info-text {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        height: 3rem;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #1565C0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None

# API endpoint
API_URL = "http://100.53.9.152:8000"  # Change this if your API is hosted elsewhere

# Helper functions
def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_URL}/health")
        return response.status_code == 200
    except:
        return False

def get_prediction(flight_data):
    """Get prediction from API"""
    try:
        response = requests.post(f"{API_URL}/predict", json=flight_data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Failed to connect to API: {str(e)}")
        return None

def format_currency(amount):
    """Format currency in Indian Rupees"""
    return f"₹{amount:,.2f}"

# Check API connection
api_healthy = check_api_health()

# Header
st.markdown('<h1 class="main-header">✈️ Flight Price Predictor</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Predict flight prices using machine learning</p>', unsafe_allow_html=True)

# API Status
if api_healthy:
    st.sidebar.success("✅ API Connected")
else:
    st.sidebar.error("❌ API Not Connected")
    st.sidebar.info("Please make sure the FastAPI server is running at http://localhost:8000")
    st.stop()

# Sidebar - Input Form
with st.sidebar:
    st.header("✈️ Flight Details")
    
    with st.form("prediction_form"):
        # Airline selection
        airline = st.selectbox(
            "Airline",
            options=[
                "IndiGo", "Air India", "Jet Airways", "SpiceJet", 
                "GoAir", "Vistara", "Air Asia", "Trujet",
                "Vistara Premium economy", "Multiple carriers",
                "Multiple carriers Premium economy", "Jet Airways Business"
            ],
            index=0
        )
        
        # Source and Destination
        col1, col2 = st.columns(2)
        with col1:
            source = st.selectbox(
                "Source",
                options=["Banglore", "Delhi", "Kolkata", "Chennai", "Mumbai"],
                index=0
            )
        with col2:
            destination = st.selectbox(
                "Destination",
                options=["New Delhi", "Banglore", "Cochin", "Kolkata", "Hyderabad", "Delhi"],
                index=0
            )
        
        # Journey Date
        min_date = datetime(2019, 1, 1)
        max_date = datetime(2019, 12, 31)
        journey_date = st.date_input(
            "Date of Journey",
            min_value=min_date,
            max_value=max_date,
            value=datetime(2019, 3, 24)
        )
        
        # Route
        route = st.text_input(
            "Route",
            value="BLR → DEL",
            help="Format: SRC → DEST (e.g., BLR → DEL)"
        )
        
        # Times
        col1, col2 = st.columns(2)
        with col1:
            dep_time = st.text_input(
                "Departure Time",
                value="22:20",
                help="Format: HH:MM"
            )
        with col2:
            arrival_time = st.text_input(
                "Arrival Time",
                value="01:10 22 Mar",
                help="Include date if next day"
            )
        
        # Duration
        duration = st.text_input(
            "Duration",
            value="2h 50m",
            help="Format: Xh Ym (e.g., 2h 50m, 19h)"
        )
        
        # Total Stops
        total_stops = st.selectbox(
            "Total Stops",
            options=["non-stop", "1 stop", "2 stops", "3 stops", "4 stops"],
            index=0
        )
        
        # Additional Info
        additional_info = st.text_input(
            "Additional Info",
            value="No info",
            help="e.g., No info, Business class"
        )
        
        # Submit button
        submitted = st.form_submit_button("🔮 Predict Price")

# Main content area
if submitted:
    with st.spinner("Predicting flight price..."):
        # Prepare data for API
        flight_data = {
            "Airline": airline,
            "Date_of_Journey": journey_date.strftime("%d/%m/%Y"),
            "Source": source,
            "Destination": destination,
            "Route": route,
            "Dep_Time": dep_time,
            "Arrival_Time": arrival_time,
            "Duration": duration,
            "Total_Stops": total_stops,
            "Additional_Info": additional_info
        }
        
        # Get prediction
        result = get_prediction(flight_data)
        
        if result:
            st.session_state.prediction_made = True
            st.session_state.prediction_result = result

# Display prediction results
if st.session_state.prediction_made and st.session_state.prediction_result:
    result = st.session_state.prediction_result
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Prediction box
        st.markdown(
            f"""
            <div class="prediction-box">
                <h2>Predicted Flight Price</h2>
                <div class="prediction-price">{format_currency(result['predicted_price'])}</div>
                <p>Confidence Interval: {format_currency(result['confidence_interval']['lower'])} - {format_currency(result['confidence_interval']['upper'])}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Flight details
        st.subheader("📋 Flight Details")
        
        # Create a nice display of input data
        input_data = result['input_data']
        cols = st.columns(5)
        details = [
            ("Airline", input_data['Airline']),
            ("From → To", f"{input_data['Source']} → {input_data['Destination']}"),
            ("Date", input_data['Date_of_Journey']),
            ("Departure", input_data['Dep_Time']),
            ("Arrival", input_data['Arrival_Time']),
            ("Duration", input_data['Duration']),
            ("Stops", input_data['Total_Stops']),
            ("Route", input_data['Route']),
            ("Additional", input_data['Additional_Info'])
        ]
        
        for i, (label, value) in enumerate(details):
            with cols[i % 5]:
                st.markdown(
                    f"""
                    <div class="feature-card">
                        <strong>{label}</strong><br>
                        {value}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    with col2:
        # Feature Importance (if available)
        if 'feature_importance' in result and result['feature_importance']:
            st.subheader("📊 Feature Importance")
            
            # Create a bar chart using plotly
            features = list(result['feature_importance'].keys())
            importance = list(result['feature_importance'].values())
            
            fig = go.Figure(data=[
                go.Bar(
                    x=importance,
                    y=features,
                    orientation='h',
                    marker=dict(
                        color=importance,
                        colorscale='Viridis',
                        showscale=True
                    )
                )
            ])
            
            fig.update_layout(
                title="Top Contributing Features",
                xaxis_title="Importance",
                yaxis_title="Features",
                height=300,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Confidence meter
        st.subheader("📈 Confidence Level")
        
        # Calculate confidence based on interval width
        price = result['predicted_price']
        interval_width = result['confidence_interval']['upper'] - result['confidence_interval']['lower']
        confidence_percentage = max(0, min(100, 100 - (interval_width / price * 50)))
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=confidence_percentage,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Confidence Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#1E88E5"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"},
                    {'range': [80, 100], 'color': "darkgray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

# Show example when no prediction made
else:
    st.info("👈 Fill in the flight details in the sidebar and click 'Predict Price' to get started!")
    
    # Show example data
    with st.expander("📝 View Example Data"):
        example_data = {
            "Airline": "IndiGo",
            "Date_of_Journey": "24/03/2019",
            "Source": "Banglore",
            "Destination": "New Delhi",
            "Route": "BLR → DEL",
            "Dep_Time": "22:20",
            "Arrival_Time": "01:10 22 Mar",
            "Duration": "2h 50m",
            "Total_Stops": "non-stop",
            "Additional_Info": "No info"
        }
        
        st.json(example_data)
        
        if st.button("🚀 Try This Example"):
            st.session_state.prediction_made = False
            # Set sidebar values (you'd need to implement this with session state)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Built with ❤️ using Streamlit and FastAPI | Flight Price Prediction Model</p>
    </div>
    """,
    unsafe_allow_html=True
)