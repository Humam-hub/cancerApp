import streamlit as st
from utils import create_sidebar_navigation
from sections.PatientManagement import patient_management_page
from sections.MealPlanner import meal_planner_page
from sections.EmotionalSupport import emotional_support_page
from sections.Quiz import cancer_quiz_page
from sections.ImageAnalysis import image_analysis_page

def home_page():
    # Create consistent navigation
    create_sidebar_navigation()

    # Add custom CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: #1E88E5;
            text-align: center;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("<h1 class='main-header'>🏥 Welcome to Cancer Care Solutions</h1>", unsafe_allow_html=True)

    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Transforming Cancer Care with AI
        
        Our platform leverages cutting-edge artificial intelligence to provide comprehensive cancer care solutions:
        
        - **Patient Management**: Personalized treatment plans and monitoring
        - **Meal Planning**: Cancer-friendly nutrition guidance
        - **Emotional Support**: AI-powered emotional companion
        - **Cancer Education**: Interactive quiz and learning resources
        
        Navigate through our modules using the sidebar to explore our innovative solutions.
        """)

    # Featured Modules Section
    st.markdown("## Our Modules")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        ### 🏥 Patient Management
        Comprehensive patient care and monitoring system
        """)
    
    with col2:
        st.markdown("""
        ### 🥗 Meal Planner
        Cancer-friendly meal planning and nutrition
        """)
    
    with col3:
        st.markdown("""
        ### 🤗 Emotional Support
        AI-powered emotional support companion
        """)

def main():
    # Must be the first Streamlit command
    st.set_page_config(
        page_title="Cancer Care Solutions",
        page_icon="🏥",
        layout="wide"
    )

    # Route to the correct page based on navigation state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'

    if st.session_state.current_page == 'home':
        home_page()
    elif st.session_state.current_page == 'patient_management':
        patient_management_page()
    elif st.session_state.current_page == 'meal_planner':
        meal_planner_page()
    elif st.session_state.current_page == 'emotional_support':
        emotional_support_page()
    elif st.session_state.current_page == 'quiz':
        cancer_quiz_page()
    elif st.session_state.current_page == 'image_analysis':
        image_analysis_page()

if __name__ == "__main__":
    main()