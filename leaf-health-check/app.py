"""
Leaf Health Check - Streamlit Web Application
Analyze plant leaf health using AI and image processing.
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import io
import json
from datetime import datetime

# Import custom modules
from utils import (
    preprocess_image, 
    detect_damaged_areas, 
    visualize_damage,
    load_image_from_bytes,
    save_results
)
from model import create_analyzer


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Leaf Health Check",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .header-style {
        color: #2ECC40;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .success-box {
        background-color: #D4EDDA;
        border-left: 5px solid #28A745;
        padding: 15px;
        border-radius: 5px;
    }
    .warning-box {
        background-color: #FFF3CD;
        border-left: 5px solid #FFC107;
        padding: 15px;
        border-radius: 5px;
    }
    .error-box {
        background-color: #F8D7DA;
        border-left: 5px solid #DC3545;
        padding: 15px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

with st.sidebar:
    st.title("⚙️ Settings")
    
    # API Key input
    st.subheader("API Configuration")
    gemini_api_key = st.text_input(
        "Enter Gemini API Key (optional)",
        type="password",
        help="Leave empty to use mock diagnosis without AI"
    )
    
    use_gemini = st.checkbox(
        "Use Gemini AI for Diagnosis",
        value=bool(gemini_api_key),
        help="Enable AI-powered diagnosis with Gemini"
    )
    
    st.divider()
    
    # Session info
    st.subheader("About")
    st.info(
        """
        **Leaf Health Check v1.0**
        
        Analyze your plant leaf health using:
        - 🤖 AI-powered diagnosis
        - 📊 Damage detection
        - 💡 Treatment recommendations
        """
    )


# ============================================================================
# MAIN APP LOGIC
# ============================================================================

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'preprocessed_image' not in st.session_state:
        st.session_state.preprocessed_image = None
    if 'damage_mask' not in st.session_state:
        st.session_state.damage_mask = None


def display_home_page():
    """Display the home/welcome page."""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("# 🍃 Leaf Health Check")
        st.markdown("### Intelligent Plant Disease Detection System")
        
        st.markdown("""
        Welcome to **Leaf Health Check**, an AI-powered system that analyzes the health of plant leaves 
        and provides detailed diagnosis and treatment recommendations.
        
        ## Key Features
        
        ✅ **Image Upload** - Upload photos of plant leaves for analysis
        
        ✅ **Damage Detection** - Automatically identify discolored or damaged areas
        
        ✅ **AI Diagnosis** - Get AI-powered disease identification and explanations
        
        ✅ **Severity Classification** - Understand damage severity (Healthy → Dying)
        
        ✅ **Smart Recommendations** - Receive specific treatment and prevention tips
        
        ✅ **Result Export** - Download analysis reports in TXT or JSON format
        
        ## How It Works
        
        1. 📤 **Upload** - Upload a clear image of a plant leaf
        2. 🔍 **Process** - The system analyzes the image for damage and discoloration
        3. 🤖 **Diagnose** - AI examines the image and damage patterns
        4. 📋 **Report** - Get detailed diagnosis with severity level and tips
        5. 💾 **Export** - Save your analysis results for future reference
        """)
    
    with col2:
        st.markdown("")
        st.markdown("")
        
        # Create a simple demo image representation
        st.info(
            """
            ### Quick Start Guide
            
            **Step 1:** Go to the 'Leaf Analysis' page
            
            **Step 2:** Upload a leaf image
            
            **Step 3:** Click 'Analyze Leaf'
            
            **Step 4:** View detailed results
            
            **Step 5:** Export if needed
            """
        )
        
        # Supported formats
        st.markdown("### Supported Formats")
        st.caption("PNG, JPG, JPEG, WebP, BMP")


def display_analysis_page():
    """Display the leaf analysis page."""
    st.title("🔍 Leaf Analysis")
    st.markdown("Upload a plant leaf image to get started with analysis")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Leaf Image")
        
        uploaded_file = st.file_uploader(
            "Choose a leaf image",
            type=["png", "jpg", "jpeg", "webp", "bmp"],
            key="leaf_image_uploader"
        )
        
        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
    
    # If image is uploaded
    if st.session_state.uploaded_file is not None:
        with col1:
            st.success("✅ Image uploaded successfully!")
            
            # Load and display the image
            image = load_image_from_bytes(st.session_state.uploaded_file)
            st.image(image, caption="Uploaded Leaf Image", use_column_width=True)
            
            # Image info
            st.markdown("**Image Info:**")
            st.text(f"Size: {image.size[0]}x{image.size[1]} pixels")
            st.text(f"Format: {image.format}")
        
        with col2:
            st.subheader("⚙️ Analysis Settings")
            
            st.markdown("**Processing Options:**")
            enhance = st.checkbox("Enhance image brightness", value=True)
            show_damage_visualization = st.checkbox("Show damage visualization", value=True)
            
            st.divider()
            
            # Analysis button
            if st.button("🚀 Analyze Leaf", use_container_width=True, type="primary"):
                with st.spinner("🔍 Analyzing leaf health..."):
                    # Preprocess image
                    image_array = np.array(image)
                    preprocessed = preprocess_image(image_array)
                    
                    # Detect damaged areas
                    damage_mask, damage_percentage = detect_damaged_areas(preprocessed)
                    
                    # Create analyzer instance
                    analyzer = create_analyzer(
                        use_gemini=use_gemini,
                        api_key=gemini_api_key
                    )
                    
                    # Analyze
                    analysis_result = analyzer.analyze_leaf(
                        damage_percentage=damage_percentage
                    )
                    
                    # Store in session state
                    st.session_state.analysis_result = analysis_result
                    st.session_state.preprocessed_image = preprocessed
                    st.session_state.damage_mask = damage_mask
                    
                    st.success("✅ Analysis complete! Scroll down to see results.")
    
    # Display analysis results
    if st.session_state.analysis_result is not None:
        st.divider()
        st.subheader("📊 Analysis Results")
        
        result = st.session_state.analysis_result
        
        # Create metrics row
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric(
                "Damage Percentage",
                f"{result['damage_percentage']:.1f}%",
                delta="Damage Level"
            )
        
        with metric_col2:
            st.metric(
                "Severity Level",
                result['severity'].upper(),
                delta=None
            )
        
        with metric_col3:
            st.metric(
                "Plant Status",
                "⚠️" if result['damage_percentage'] > 20 else "✅",
                delta=None
            )
        
        st.divider()
        
        # Severity description
        severity_colors = {
            'healthy': '✅ Healthy',
            'mild': '⚠️ Mild',
            'moderate': '🟠 Moderate',
            'severe': '🔴 Severe',
            'dying': '💀 Dying'
        }
        
        st.markdown(f"### {severity_colors.get(result['severity'], result['severity'])}")
        st.markdown(f"*{result['severity_description']}*")
        
        st.divider()
        
        # Diagnosis section
        st.subheader("🤖 AI Diagnosis")
        
        col_diagnosis1, col_diagnosis2 = st.columns([1, 1])
        
        with col_diagnosis1:
            st.markdown("**Disease Identified:**")
            st.markdown(f"### {result['disease_name']}")
        
        with col_diagnosis2:
            st.markdown("**Description:**")
            st.markdown(result['explanation'])
        
        st.divider()
        
        # Treatment recommendations
        st.subheader("💡 Treatment Recommendations")
        
        tips = result['tips']
        for i, tip in enumerate(tips, 1):
            st.markdown(f"**{i}. {tip}**")
        
        st.divider()
        
        # Visualization section
        if st.session_state.damage_mask is not None and show_damage_visualization:
            st.subheader("🔍 Damage Visualization")
            
            viz_col1, viz_col2 = st.columns(2)
            
            with viz_col1:
                # Display preprocessed image
                if st.session_state.preprocessed_image is not None:
                    prep_img = (st.session_state.preprocessed_image * 255).astype(np.uint8)
                    st.image(prep_img, caption="Preprocessed Image", use_column_width=True)
            
            with viz_col2:
                # Display damage mask
                st.image(
                    st.session_state.damage_mask,
                    caption="Detected Damage Areas (Red = Damaged)",
                    use_column_width=True,
                    clamp=True
                )
            
            # Create and display visualization overlay
            if st.session_state.preprocessed_image is not None:
                viz_overlay = visualize_damage(
                    st.session_state.preprocessed_image,
                    st.session_state.damage_mask
                )
                st.image(
                    viz_overlay,
                    caption="Damage Overlay Visualization",
                    use_column_width=True
                )
        
        st.divider()
        
        # Export results section
        st.subheader("💾 Export Results")
        
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            # TXT export
            txt_result = save_results(
                result['damage_percentage'],
                result['severity'],
                f"{result['disease_name']}: {result['explanation']}",
                result['tips'],
                format='txt'
            )
            
            st.download_button(
                label="📄 Download as TXT",
                data=txt_result,
                file_name=f"leaf_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with export_col2:
            # JSON export
            json_result = save_results(
                result['damage_percentage'],
                result['severity'],
                f"{result['disease_name']}: {result['explanation']}",
                result['tips'],
                format='json'
            )
            
            st.download_button(
                label="📋 Download as JSON",
                data=json_result,
                file_name=f"leaf_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )


def display_test_mode():
    """Display testing/demo mode with sample functionality."""
    st.subheader("🧪 Test Mode")
    
    st.info("Generate a test image with simulated damage for demo purposes.")
    
    if st.button("Generate Test Image", use_container_width=True):
        # Create a synthetic leaf image with damage
        img = np.ones((224, 224, 3), dtype=np.uint8) * 50  # Green-ish background
        
        # Add "leaf" shape
        for i in range(224):
            for j in range(224):
                dist = np.sqrt((i - 112) ** 2 + (j - 112) ** 2)
                if dist < 80:
                    img[i, j] = [34, 139, 34]  # Forest green
        
        # Add some yellow spots (damage)
        cv2.circle(img, (80, 80), 20, (0, 255, 255), -1)      # Yellow
        cv2.circle(img, (150, 100), 15, (0, 255, 255), -1)    # Yellow
        
        # Add brown spots
        cv2.circle(img, (120, 140), 25, (0, 165, 255), -1)    # Brown
        
        # Convert to PIL and display
        test_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        st.image(test_image, caption="Synthetic Test Leaf (with simulated damage)", use_column_width=True)
        
        st.success("Test image generated! You can now use this for analysis testing.")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main application entry point."""
    
    # Initialize session state
    initialize_session_state()
    
    # Create navigation using tabs
    tab1, tab2, tab3 = st.tabs(["🏠 Home", "📊 Analysis", "🧪 Test"])
    
    with tab1:
        display_home_page()
    
    with tab2:
        display_analysis_page()
    
    with tab3:
        display_test_mode()
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #666; margin-top: 20px;'>
            <p><small>Leaf Health Check © 2024 | AI-Powered Plant Disease Detection</small></p>
        </div>
        """,
        unsafe_allow_html=True
    )


# Run the application
if __name__ == "__main__":
    main()
