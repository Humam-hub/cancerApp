import streamlit as st
from utils import create_sidebar_navigation, initialize_groq_client, get_ai_response

def analyze_emotion_and_generate_support(message):
    """
    Analyze emotional content and generate supportive response using Groq API.
    
    Args:
        message (str): User's message
    
    Returns:
        str: Supportive AI response
    """
    client = initialize_groq_client()
    if not client:
        return "Error: Unable to initialize AI client"

    prompt = f"""
    As a compassionate AI companion for someone affected by cancer, carefully consider this message:
    "{message}"
    
    Provide a warm, empathetic response that:
    1. Acknowledges their emotions with genuine understanding
    2. Offers specific comfort based on their situation
    3. Suggests a practical coping strategy
    4. Includes relevant scientific insights when appropriate
    5. Ends with words of encouragement
    
    Keep the tone gentle, supportive, and hopeful.
    """
    
    return get_ai_response(client, prompt)

def emotional_support_page():
    # Create consistent navigation
    create_sidebar_navigation()
    
    st.title("🤗 Emotional Support Companion")
    
    # Introduction
    st.markdown("""
    ### A Safe Space for Your Journey
    Share your thoughts and feelings openly. This AI companion is here to listen, 
    understand, and provide supportive guidance through your cancer journey.
    """)
    
    # Message Input Section
    with st.form("emotion_support_form"):
        user_message = st.text_area(
            "Share what's on your mind...",
            height=150,
            placeholder="I'm feeling overwhelmed with everything happening..."
        )
        
        submitted = st.form_submit_button("Get Support")
    
    if submitted and user_message:
        with st.spinner("Processing your message with care..."):
            support_response = analyze_emotion_and_generate_support(user_message)
            
            # Display response in a styled container
            st.markdown("### Your AI Companion's Response")
            st.info(support_response)
    
    # Quick Access Support Tools
    st.markdown("### 🧘‍♀️ Support Tools")
    support_tool = st.selectbox(
        "Select a support tool:",
        ["Breathing Exercise", "Guided Relaxation", "Positive Affirmations"]
    )
    
    # Display selected tool content
    if support_tool == "Breathing Exercise":
        st.markdown("""
        #### 4-7-8 Breathing Technique
        1. Find a comfortable position
        2. Inhale quietly through your nose for 4 counts
        3. Hold your breath for 7 counts
        4. Exhale completely through your mouth for 8 counts
        5. Repeat 4 times
        
        *This technique helps reduce anxiety and promote relaxation.*
        """)
    
    elif support_tool == "Guided Relaxation":
        st.markdown("""
        #### Progressive Relaxation
        1. Start with your toes, tense them for 5 seconds
        2. Release and notice the relaxation
        3. Move to your feet, then ankles
        4. Continue up through your body
        5. End with your face and head
        
        *Take 10-15 minutes to complete this exercise.*
        """)
    
    else:
        st.markdown("""
        #### Daily Affirmations
        - "I am stronger than I know"
        - "Each day brings new healing"
        - "I am surrounded by support"
        - "My body knows how to heal"
        - "I choose hope and healing"
        
        *Repeat these affirmations throughout your day.*
        """)
    
    # Emergency Resources
    st.markdown("### 🆘 24/7 Support Resources")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            #### Immediate Support
            - Cancer Support Helpline: 1-800-227-2345
            - Crisis Line: 1-800-273-8255
            - Emergency: 911
        """)
    
    with col2:
        st.markdown("""
            #### Online Resources
            - [Cancer.org Support](https://www.cancer.org/support-programs-and-services.html)
            - [CancerCare.org](https://www.cancercare.org/counseling)
            - [Cancer Support Community](https://www.cancersupportcommunity.org/)
        """)

if __name__ == "__main__":
    emotional_support_page() 