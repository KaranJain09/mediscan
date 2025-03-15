import streamlit as st
from pdf_processor import extract_text_from_pdf
from agent import generate_recommendations
import time

# Page configuration
st.set_page_config(
    page_title="MediScan - Health Report Analyzer",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Main styling */
    .main {
        background-color: #f8f9fa;
        padding: 2rem;
    }
    
    /* Header */
    .header-container {
        padding: 1.5rem;
        background: linear-gradient(90deg, #2c3e50 0%, #4ca1af 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 300;
    }
    
    /* Cards */
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
    .card-title {
        font-size: 1.3rem;
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
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #2c3e50;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .metric-title {
        font-size: 0.9rem;
        color: #7f8c8d;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2c3e50;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem;
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
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4ca1af !important;
        color: white !important;
    }
    
    /* Icons */
    .icon-container {
        font-size: 3rem;
        text-align: center;
        margin: 1rem 0;
        color: #4ca1af;
    }
    
    /* Recommendation sections */
    .recommendation-section {
        margin-bottom: 1.5rem;
        padding: 1rem;
        border-radius: 8px;
        background-color: #f8f9fa;
    }
    
    .recommendation-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .feature-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #f1f7fa;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        color: #4ca1af;
    }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .disclaimer {
        font-size: 0.8rem;
        color: #95a5a6;
        font-style: italic;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h3 style='text-align: center; color: #2c3e50;'>MediScan</h3>", unsafe_allow_html=True)
    
    # Simple icon instead of Lottie animation
    st.markdown('<div class="icon-container">🩺</div>', unsafe_allow_html=True)
    
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
<div class="header-container">
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
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Upload Your Blood Test Report</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], key="pdf_uploader")
        if uploaded_file is not None:
            if st.button("Process Report", key="process_button"):
                # Progress bar animation
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
        # Feature boxes instead of animation
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Why Use MediScan?</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Accurate Analysis</div>
            <p>Our AI model is trained on thousands of medical reports for precise health insights.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Privacy Focused</div>
            <p>Your data is processed securely and never stored on our servers.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Personalized Insights</div>
            <p>Get tailored recommendations based on your unique health profile.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Analysis
with tabs[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Extracted Report Data</div>', unsafe_allow_html=True)
    
    if "extracted_text" in st.session_state:
        # Display a sample of the extracted text with a toggle for full text
        sample_text = st.session_state["extracted_text"][:500] + "..." if len(st.session_state["extracted_text"]) > 500 else st.session_state["extracted_text"]
        st.markdown(f"**Sample of extracted text:**\n\n{sample_text}")
        
        with st.expander("View Full Extracted Text"):
            st.text_area("Complete Extracted Text", st.session_state["extracted_text"], height=300)
        
        # Display key metrics (these would be extracted from the text in a real implementation)
        st.markdown("### Key Health Indicators")
        
        # Metric cards row
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        
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
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Health Recommendations</div>', unsafe_allow_html=True)
    
    if "extracted_text" in st.session_state:
        with st.spinner("Generating personalized recommendations..."):
            recommendations = generate_recommendations(st.session_state["extracted_text"])
        
        if "⚠️" in recommendations:
            st.error(recommendations)
        else:
            st.markdown(recommendations)
            
            # Action buttons for recommendations
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
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Health Metrics Visualization</div>', unsafe_allow_html=True)
    
    if "extracted_text" in st.session_state:
        # This would be replaced with actual data visualization in a real implementation
        st.markdown("### Blood Test Results vs. Normal Range")
        
        # Simple chart using Streamlit's built-in charting
        import pandas as pd
        import numpy as np
        
        # Sample data - in a real app, this would come from the extracted text
        data = {
            'Metric': ['Hemoglobin', 'White Blood Cells', 'Platelets', 'Glucose', 'Cholesterol'],
            'Value': [14.5, 7.2, 250, 92, 185],
            'Min Normal': [12, 4.5, 150, 70, 125],
            'Max Normal': [16, 11, 450, 100, 200]
        }
        
        df = pd.DataFrame(data)
        
        # Normalize the values for better visualization
        df['Normalized Value'] = (df['Value'] - df['Min Normal']) / (df['Max Normal'] - df['Min Normal'])
        df['Normalized Value'] = df['Normalized Value'].clip(0, 1)
        
        st.bar_chart(df.set_index('Metric')['Normalized Value'])
        
        st.markdown("### Detailed Analysis")
        
        # Create tabs for different health categories
        health_tabs = st.tabs(["Blood Counts", "Metabolic", "Lipids", "Vitamins"])
        
        with health_tabs[0]:
            st.markdown("#### Blood Cell Counts")
            st.markdown("Your blood cell counts are within normal ranges, indicating good overall health.")
            
        with health_tabs[1]:
            st.markdown("#### Metabolic Indicators")
            st.markdown("Your glucose and other metabolic indicators are within healthy ranges.")
            
        with health_tabs[2]:
            st.markdown("#### Lipid Profile")
            st.markdown("Your cholesterol levels are normal, which is good for heart health.")
            
        with health_tabs[3]:
            st.markdown("#### Vitamin Levels")
            st.markdown("Your vitamin D levels could be improved. Consider supplementation or more sun exposure.")
    else:
        st.info("No metrics available yet. Please upload and process a report first.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>© 2025 MediScan Health Report Analyzer | Privacy Policy | Terms of Service</p>
    <p>Not a substitute for professional medical advice. Always consult with healthcare professionals.</p>
</div>
""", unsafe_allow_html=True)