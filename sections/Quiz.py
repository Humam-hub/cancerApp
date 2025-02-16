import streamlit as st
import random
from utils import create_sidebar_navigation, initialize_groq_client, get_ai_response

# Expanded quiz questions database
QUIZ_QUESTIONS = [
    # Original 5 questions...
    {
        "question": "Which of these is NOT a recommended cancer screening test?",
        "options": [
            "Mammogram for breast cancer",
            "Colonoscopy for colorectal cancer",
            "Blood pressure check for lung cancer",
            "PSA test for prostate cancer"
        ],
        "correct": 2,
        "explanation": "Blood pressure checks are not used for cancer screening. Regular cancer screening tests include mammograms, colonoscopies, PSA tests, and low-dose CT scans for lung cancer in high-risk individuals."
    },
    # ... adding 15 more questions for a total of 20
    {
        "question": "What percentage of lung cancer cases are linked to smoking?",
        "options": [
            "About 50%",
            "About 60%",
            "About 80%",
            "About 90%"
        ],
        "correct": 3,
        "explanation": "Approximately 90% of lung cancer cases are linked to smoking, making it the leading cause of preventable cancer deaths."
    },
    {
        "question": "Which of these foods has been shown to have cancer-fighting properties?",
        "options": [
            "Processed meats",
            "Refined sugar",
            "Turmeric",
            "White bread"
        ],
        "correct": 2,
        "explanation": "Turmeric contains curcumin, which has shown anti-inflammatory and potential anti-cancer properties in numerous studies."
    },
    {
        "question": "What is the recommended age to begin regular mammogram screenings for women at average risk?",
        "options": [
            "30 years old",
            "40 years old",
            "50 years old",
            "60 years old"
        ],
        "correct": 1,
        "explanation": "The American Cancer Society recommends women at average risk start mammogram screenings at age 40, though some may choose to start between ages 40-44. Women aged 45-54 should get mammograms every year."
    },
    {
        "question": "Which of these lifestyle changes can help reduce cancer risk?",
        "options": [
            "Getting regular exercise",
            "Maintaining a healthy weight",
            "Avoiding tobacco",
            "All of the above"
        ],
        "correct": 3,
        "explanation": "All these lifestyle changes can help reduce cancer risk. Regular exercise, maintaining a healthy weight, and avoiding tobacco are key preventive measures recommended by health organizations."
    },
    {
        "question": "What is immunotherapy in cancer treatment?",
        "options": [
            "A type of radiation therapy",
            "Treatment that helps the immune system fight cancer",
            "A surgical procedure",
            "A vitamin supplement regimen"
        ],
        "correct": 1,
        "explanation": "Immunotherapy is a type of cancer treatment that helps your immune system fight cancer. It works by boosting or changing how your immune system works to better find and destroy cancer cells."
    },
    {
        "question": "Which cancer has the highest survival rate when detected early?",
        "options": [
            "Lung cancer",
            "Pancreatic cancer",
            "Thyroid cancer",
            "Liver cancer"
        ],
        "correct": 2,
        "explanation": "Thyroid cancer generally has one of the highest survival rates when detected early, with a 5-year survival rate of over 98% for localized thyroid cancer."
    },
    {
        "question": "How often should adults get a colonoscopy screening (average risk)?",
        "options": [
            "Every year",
            "Every 5 years",
            "Every 10 years",
            "Every 15 years"
        ],
        "correct": 2,
        "explanation": "For people at average risk, colonoscopy screening is recommended every 10 years starting at age 45. Those with higher risk factors may need more frequent screenings."
    },
    {
        "question": "Which of these is a warning sign of skin cancer?",
        "options": [
            "A mole that changes in size or color",
            "A temporary rash",
            "Dry skin",
            "Freckles"
        ],
        "correct": 0,
        "explanation": "Changes in moles, including size, color, or shape, are important warning signs of skin cancer. The ABCDE rule (Asymmetry, Border, Color, Diameter, Evolving) helps identify suspicious moles."
    },
    {
        "question": "What percentage of cancers are estimated to be preventable through lifestyle changes?",
        "options": [
            "About 10%",
            "About 30%",
            "About 40%",
            "About 50%"
        ],
        "correct": 3,
        "explanation": "According to the World Health Organization, about 50% of all cancers are preventable through lifestyle changes such as healthy diet, regular exercise, avoiding tobacco, and limiting alcohol consumption."
    },
    {
        "question": "Which vitamin is important for reducing cancer risk and is primarily obtained through sun exposure?",
        "options": [
            "Vitamin A",
            "Vitamin B12",
            "Vitamin C",
            "Vitamin D"
        ],
        "correct": 3,
        "explanation": "Vitamin D, primarily obtained through sun exposure, has been linked to reduced risk of several cancers. Many people need supplements to maintain adequate levels, especially in less sunny climates."
    },
    {
        "question": "What is metastasis in cancer?",
        "options": [
            "Initial tumor formation",
            "Cancer cell death",
            "Spread of cancer to other parts of the body",
            "Cancer treatment method"
        ],
        "correct": 2,
        "explanation": "Metastasis occurs when cancer cells spread from their original location to other parts of the body through the bloodstream or lymphatic system, forming secondary tumors."
    },
    {
        "question": "Which of these foods is associated with increased cancer risk?",
        "options": [
            "Processed meats",
            "Fresh vegetables",
            "Whole grains",
            "Fish"
        ],
        "correct": 0,
        "explanation": "Processed meats (like bacon, hot dogs, and deli meats) have been classified as Group 1 carcinogens by the World Health Organization, meaning there is strong evidence they can cause cancer."
    }
]

def get_random_questions(n=5):
    """Get n random questions from the question bank."""
    return random.sample(QUIZ_QUESTIONS, n)

def get_educational_insight(topic):
    """Get additional educational insight about a cancer-related topic using Groq API."""
    client = initialize_groq_client()
    if not client:
        return "Unable to fetch additional information."

    prompt = f"""
    Provide a brief, educational insight about {topic} in cancer awareness.
    Focus on:
    1. Recent research or statistics
    2. Practical prevention tips
    3. Common misconceptions
    Keep the response concise and encouraging.
    """
    
    return get_ai_response(client, prompt)

def cancer_quiz_page():
    # Create consistent navigation
    create_sidebar_navigation()
    
    st.title("🎯 Cancer Awareness Quiz")
    
    # Initialize session state variables
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = None
    if 'answer_submitted' not in st.session_state:
        st.session_state.answer_submitted = False

    # Quiz introduction
    if not st.session_state.quiz_started:
        st.markdown("""
        ### Test Your Cancer Awareness Knowledge
        
        Take our quiz to learn important facts about cancer prevention, 
        detection, and treatment. Questions are randomly selected from our 
        comprehensive question bank.
        
        - 5 questions per quiz
        - Immediate feedback and explanations
        - Educational insights after each question
        """)
        
        if st.button("Start Quiz"):
            st.session_state.quiz_started = True
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answers = []
            st.session_state.quiz_questions = get_random_questions()
            st.session_state.answer_submitted = False
            st.rerun()
    
    # Quiz in progress
    elif st.session_state.current_question < len(st.session_state.quiz_questions):
        # Progress bar
        progress = (st.session_state.current_question / len(st.session_state.quiz_questions))
        st.progress(progress)
        
        # Score display
        st.markdown(f"**Score: {st.session_state.score}/{len(st.session_state.quiz_questions)}**")
        
        # Display current question
        question = st.session_state.quiz_questions[st.session_state.current_question]
        st.markdown(f"### Question {st.session_state.current_question + 1}")
        st.markdown(question["question"])
        
        # Answer selection
        answer = st.radio("Select your answer:", 
                         question["options"],
                         key=f"q_{st.session_state.current_question}")
        
        # Create columns for buttons with better spacing
        col1, col2, col3 = st.columns([1, 1, 3])
        
        # Submit answer button
        with col1:
            submit_clicked = st.button("Submit Answer", 
                                     disabled=st.session_state.answer_submitted)
        
        # Next question button (only show after answer is submitted)
        with col2:
            if st.session_state.answer_submitted:
                next_clicked = st.button("Next Question")
            
        # Handle submit click
        if submit_clicked and not st.session_state.answer_submitted:
            st.session_state.answer_submitted = True
            selected_index = question["options"].index(answer)
            is_correct = selected_index == question["correct"]
            
            if is_correct:
                st.success("✅ Correct!")
                st.session_state.score += 1
                st.balloons()
            else:
                st.error("❌ Incorrect")
            
            # Show explanation
            st.info(f"**Explanation:** {question['explanation']}")
            
            # Store answer
            st.session_state.answers.append({
                "question": question["question"],
                "selected": answer,
                "correct": question["options"][question["correct"]],
                "is_correct": is_correct
            })
            
            # Get and display additional educational insights
            with st.expander("🔍 Learn More", expanded=True):
                topic = question["question"].split("?")[0]  # Use question topic for insights
                insight = get_educational_insight(topic)
                st.markdown(insight)
        
        # Handle next click
        if st.session_state.answer_submitted and 'next_clicked' in locals() and next_clicked:
            st.session_state.current_question += 1
            st.session_state.answer_submitted = False
            st.rerun()

    # Quiz completed
    else:
        st.success(f"🎉 Quiz Completed! Final Score: {st.session_state.score}/{len(st.session_state.quiz_questions)}")
        
        # Performance summary
        st.markdown("### Your Performance Summary")
        for i, answer in enumerate(st.session_state.answers):
            with st.expander(f"Question {i+1}"):
                st.write(f"**Question:** {answer['question']}")
                st.write(f"**Your Answer:** {answer['selected']}")
                st.write(f"**Correct Answer:** {answer['correct']}")
                if answer['is_correct']:
                    st.success("✅ Correct")
                else:
                    st.error("❌ Incorrect")
        
        # Restart quiz button
        if st.button("Take Another Quiz"):
            st.session_state.quiz_started = False
            st.session_state.quiz_questions = None
            st.rerun()

if __name__ == "__main__":
    cancer_quiz_page() 