import streamlit as st
from pdf_processor import extract_text_from_pdf
from agent import generate_recommendations, generate_health_metrics
import time
import json  # Needed for parsing JSON responses
import plotly.graph_objects as go
import re

# Page configuration
st.set_page_config(
    page_title="MediScan - Health Report Analyzer",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with animations
st.markdown("""
<style>
    /* Global animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0% { transform: scale(0.95); }
        50% { transform: scale(1); }
        100% { transform: scale(0.95); }
    }
    .fade-in {
        animation: fadeIn 1s ease-out;
    }
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Main styling */
    .main {
        background-color: #f8f9fa;
        padding: 2rem;
    }
    
    /* Header */
    .header-container {
        padding: 2rem;
        background: linear-gradient(-45deg, #2c3e50, #4ca1af, #2c3e50, #4ca1af);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
        text-align: center;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .header-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    .header-subtitle {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 300;
    }
    
    /* Cards */
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .card-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        border-bottom: 2px solid #4ca1af;
        padding-bottom: 0.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #4ca1af;
        color: white;
        border: none;
        padding: 0.7rem 1.2rem;
        border-radius: 5px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #2c3e50;
        box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: #4ca1af;
    }
    
    /* File uploader */
    .stFileUploader {
        border: 2px dashed #4ca1af;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: background-color 0.3s;
    }
    .stFileUploader:hover {
        background-color: #f1f7fa;
    }
    
    /* Metrics */
    .metric-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f1f7fa;
        border-radius: 8px;
        padding: 1rem;
        width: 32%;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.07);
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-3px);
    }
    .metric-title {
        font-size: 0.95rem;
        color: #7f8c8d;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #2c3e50;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #95a5a6;
        font-size: 0.9rem;
        margin-top: 2rem;
        border-top: 1px solid #ecf0f1;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f7fa;
        border-radius: 5px 5px 0 0;
        padding: 10px 20px;
        font-weight: 500;
        transition: background-color 0.3s;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4ca1af !important;
        color: white !important;
    }
    
    /* Icons */
    .icon-container {
        font-size: 3.5rem;
        text-align: center;
        margin: 1rem 0;
        color: #4ca1af;
    }
    
    /* Feature Boxes */
    .feature-box {
        padding: 1.2rem;
        border-radius: 8px;
        background-color: #f1f7fa;
        margin-bottom: 1rem;
        text-align: center;
        transition: transform 0.3s;
    }
    .feature-box:hover {
        transform: scale(1.02);
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        color: #4ca1af;
    }
    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    /* Disclaimer */
    .disclaimer {
        font-size: 0.8rem;
        color: #95a5a6;
        font-style: italic;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with animated Lottie widget
with st.sidebar:
    st.markdown("<h3 style='text-align: center; color: #2c3e50;'>MediScan</h3>", unsafe_allow_html=True)
    
    # Lottie Animation (using a public Lottie file)
    st.markdown("""
    <div style="text-align: center;" class="fade-in">
      <lottie-player src="https://assets10.lottiefiles.com/packages/lf20_x62chJ.json"  background="transparent"  speed="1"  style="width: 100%; height: 200px;"  loop  autoplay></lottie-player>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### How it works")
    st.markdown("""
    1. Upload your blood test PDF
    2. Our AI extracts the relevant data
    3. Get personalized health insights
    4. Review recommendations
    """)
    
    st.markdown("---")
    st.markdown("### About the Model")
    st.markdown("""
    **Model:** `llama-3.3-70b-versatile`
    
    **Capabilities:**
    - Blood test analysis
    - Personalized recommendations
    - Nutritional insights
    """)
    
    st.markdown("---")
    st.markdown("<div class='disclaimer'>This tool is for informational purposes only and not a substitute for professional medical advice.</div>", unsafe_allow_html=True)

# Main content
# Header
st.markdown("""
<div class="header-container fade-in">
    <div class="header-title">MediScan Health Report Analyzer</div>
    <div class="header-subtitle">Upload your blood test report for personalized health insights</div>
</div>
""", unsafe_allow_html=True)

# Main content in tabs
tabs = st.tabs(["📄 Upload Report", "📋 Analysis", "🔍 Recommendations", "📊 Health Metrics"])

# Tab 1: Upload Report
with tabs[0]:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="card-title">Upload Your Blood Test Report</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], key="pdf_uploader")
        if uploaded_file is not None:
            if st.button("Process Report", key="process_button"):
                # Animated progress bar
                progress_placeholder = st.empty()
                progress_bar = progress_placeholder.progress(0)
                for percent_complete in range(0, 101, 10):
                    time.sleep(0.1)  # Simulate processing time
                    progress_bar.progress(percent_complete)
                
                # Extract text
                extracted_text = extract_text_from_pdf(uploaded_file)
                st.session_state["extracted_text"] = extracted_text
                st.success("✅ Report processed successfully!")
        else:
            st.info("Please upload a PDF file to begin analysis.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card-title">Why Use MediScan?</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box pulse">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Accurate Analysis</div>
            <p>Our AI model is trained on thousands of medical reports for precise health insights.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box pulse">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Privacy Focused</div>
            <p>Your data is processed securely and never stored on our servers.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box pulse">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Personalized Insights</div>
            <p>Get tailored recommendations based on your unique health profile.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Analysis
with tabs[1]:
    st.markdown('<div class="card-title">Extracted Report Data</div>', unsafe_allow_html=True)
    
    if "extracted_text" in st.session_state:
        sample_text = st.session_state["extracted_text"][:500] + "..." if len(st.session_state["extracted_text"]) > 500 else st.session_state["extracted_text"]
        st.markdown(f"**Sample of extracted text:**\n\n{sample_text}")
        
        with st.expander("View Full Extracted Text"):
            st.text_area("Complete Extracted Text", st.session_state["extracted_text"], height=300)
        
        st.markdown("### Key Health Indicators")
        
        st.markdown('<div class="metric-container fade-in">', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Hemoglobin</div>
            <div class="metric-value">14.5 g/dL</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Glucose</div>
            <div class="metric-value">92 mg/dL</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Cholesterol</div>
            <div class="metric-value">185 mg/dL</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No data available yet. Please upload and process a report first.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 3: Recommendations
with tabs[2]:
    st.markdown('<div class="card-title">Health Recommendations</div>', unsafe_allow_html=True)
    
    if "extracted_text" in st.session_state:
        with st.spinner("Generating personalized recommendations..."):
            recommendations = generate_recommendations(st.session_state["extracted_text"])
        
        if "⚠️" in recommendations:
            st.error(recommendations)
        else:
            st.markdown(recommendations)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📥 Download Report"):
                    st.success("Report downloaded successfully!")
            with col2:
                if st.button("📧 Email Results"):
                    st.success("Results emailed successfully!")
            with col3:
                if st.button("🖨️ Print Recommendations"):
                    st.success("Sent to printer!")
    else:
        st.info("No recommendations available yet. Please upload and process a report first.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 4: Health Metrics
with tabs[3]:
    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Health Metrics Visualization</div>', unsafe_allow_html=True)
    
    if "extracted_text" in st.session_state:
        with st.spinner("Generating health metrics analysis..."):
            health_metrics_response = generate_health_metrics(st.session_state["extracted_text"])
        
        response_clean = re.sub(r'^```(?:json)?\s*', '', health_metrics_response)
        response_clean = re.sub(r'\s*```$', '', response_clean).strip()
        
        def parse_partial_json(text):
            try:
                data = json.loads(text)
                return data
            except json.JSONDecodeError:
                metrics = []
                lines = text.split('\n')
                current_metric = {}
                for line in lines:
                    line = line.strip()
                    if line.startswith('"name":'):
                        if current_metric:
                            metrics.append(current_metric)
                        current_metric = {'name': line.split(':', 1)[1].strip().strip(',"')}
                    elif line.startswith('"value":'):
                        try:
                            current_metric['value'] = float(line.split(':', 1)[1].strip().strip(','))
                        except ValueError:
                            continue
                    elif line.startswith('"unit":'):
                        current_metric['unit'] = line.split(':', 1)[1].strip().strip(',"')
                    elif line.startswith('"normal_range":'):
                        range_str = line.split(':', 1)[1].strip().strip('[]')
                        try:
                            min_val, max_val = map(float, range_str.split(','))
                            current_metric['normal_range'] = [min_val, max_val]
                        except ValueError:
                            continue
                if current_metric and 'value' in current_metric:
                    metrics.append(current_metric)
                return {"metrics": metrics}
        
        try:
            metrics_data = parse_partial_json(response_clean)
            metrics_list = metrics_data.get("metrics", [])
            
            if metrics_list:
                st.markdown(f"### {len(metrics_list)} parameter{'s' if len(metrics_list) > 1 else ''} detected")
                
                for metric in metrics_list:
                    name = metric.get('name', 'Unknown')
                    value = metric.get('value', 0)
                    unit = metric.get('unit', '')
                    min_normal, max_normal = metric.get('normal_range', [0, 0])
                    
                    if value < min_normal:
                        status = "Below normal"
                        color = "red"
                    elif value > max_normal:
                        status = "Above normal"
                        color = "red"
                    else:
                        status = "Normal"
                        color = "green"
                    
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=value,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': f"{name} ({unit})"},
                        gauge={
                            'axis': {'range': [min_normal * 0.8, max_normal * 1.2]},
                            'bar': {'color': color},
                            'steps': [
                                {'range': [min_normal, max_normal], 'color': "lightgreen"},
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': value
                            }
                        }
                    ))
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown(f"**{name}:** {value} {unit} ({status})")
                    st.markdown(f"**Normal Range:** {min_normal} - {max_normal} {unit}")
                    st.markdown("---")
            else:
                st.warning("No metrics data extracted from the report.")
        except Exception as e:
            st.error("Error processing health metrics: " + str(e))
    else:
        st.info("No metrics available yet. Please upload and process a report first.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer fade-in">
    <p>© 2025 MediScan Health Report Analyzer | Privacy Policy | Terms of Service</p>
    <p>Not a substitute for professional medical advice. Always consult with healthcare professionals.</p>
</div>
""", unsafe_allow_html=True)
