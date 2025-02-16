import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

# Load environment variables
load_dotenv()

def initialize_groq_client():
    """Initialize and return Groq client."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    return Groq(api_key=api_key)

def get_ai_response(client, prompt, model="deepseek-r1-distill-llama-70b"):
    """Get response from DeepSeek AI via Groq."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            temperature=0.7,
            max_tokens=3500
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error getting AI response: {str(e)}"

def validate_patient_data(data):
    """Validate patient data inputs."""
    required_fields = ['name', 'age', 'cancer_type']
    return all(field in data and data[field] for field in required_fields)

def generate_treatment_plan(patient_data):
    """Generate a treatment plan based on patient data."""
    prompt = f"""
    Generate a comprehensive cancer treatment plan for:
    Patient Age: {patient_data['age']}
    Cancer Type: {patient_data['cancer_type']}
    Stage: {patient_data.get('stage', 'Unknown')}
    Please include recommended treatments, monitoring schedule, and support services.
    """
    client = initialize_groq_client()
    return get_ai_response(client, prompt)

def create_sidebar_navigation():
    """Create consistent sidebar navigation across all pages."""
    import streamlit as st

    # Hide the default sidebar navigation
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            padding-top: 2rem;
        }
        .css-1d391kg {
            padding-top: 3rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Define pages and their functions
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'

    pages = {
        'home': '🏥 Home',
        'patient_management': '📋 Patient Records',
        'meal_planner': '🍽️ Nutrition Guide',
        'emotional_support': '💝 Support Chat',
        'quiz': '📚 Learn & Quiz',
        'image_analysis': '🔬 Image Analysis'
    }

    # Create sidebar navigation
    for page_id, title in pages.items():
        if st.sidebar.button(title, key=f"nav_{page_id}"):
            st.session_state.current_page = page_id