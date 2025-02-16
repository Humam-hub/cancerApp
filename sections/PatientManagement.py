import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from utils import initialize_groq_client, get_ai_response, create_sidebar_navigation

# Initialize session state variables if they don't exist
if 'follow_up_data' not in st.session_state:
    st.session_state.follow_up_data = []
if 'reminders' not in st.session_state:
    st.session_state.reminders = []

def generate_treatment_plan(patient_data):
    """
    Generate a personalized treatment plan using the DeepSeek model via Groq API.
    
    Args:
        patient_data (dict): Dictionary containing patient information
    
    Returns:
        str: Generated treatment plan
    """
    client = initialize_groq_client()
    if not client:
        return "Error: Unable to initialize AI client"

    prompt = f"""
    Generate a comprehensive cancer treatment plan for a patient with the following characteristics:
    - Age: {patient_data['age']}
    - Gender: {patient_data['gender']}
    - Cancer Type: {patient_data['cancer_type']}
    - Stage: {patient_data['stage']}
    - Current Treatment: {patient_data['current_treatment']}
    - Symptoms: {patient_data['symptoms']}
    - Medical History: {patient_data['medical_history']}

    Please provide a detailed treatment plan including:
    1. Recommended treatment approach
    2. Medication schedule
    3. Lifestyle modifications
    4. Follow-up schedule
    5. Potential side effects and management strategies
    """
    
    return get_ai_response(client, prompt)

def generate_support_recommendations(patient_data, symptoms):
    """
    Generate support recommendations based on patient data and symptoms.
    
    Args:
        patient_data (dict): Dictionary containing patient information
        symptoms (list): List of current symptoms and side effects
    
    Returns:
        str: Support recommendations
    """
    client = initialize_groq_client()
    if not client:
        return "Error: Unable to initialize AI client"

    # Get current treatment safely with a default value
    current_treatment = patient_data.get('current_treatment', ['None'])
    if isinstance(current_treatment, list):
        current_treatment = ', '.join(current_treatment)

    prompt = f"""
    Provide comprehensive support recommendations for a cancer patient with:
    - Current Treatment: {current_treatment}
    - Current Symptoms: {', '.join(symptoms)}
    
    Include:
    1. Physical symptom management strategies
    2. Mental health support suggestions
    3. Lifestyle and dietary recommendations
    4. Support group and resource recommendations
    """
    
    return get_ai_response(client, prompt)

def create_symptom_tracker_chart(follow_up_data):
    """
    Create a line chart showing symptom severity over time.
    
    Args:
        follow_up_data (list): List of follow-up records
    
    Returns:
        plotly.graph_objects.Figure: Line chart of symptom progression
    """
    if not follow_up_data:
        return None
        
    df = pd.DataFrame(follow_up_data)
    df['date'] = pd.to_datetime(df['date'])
    
    fig = go.Figure()
    
    # Get all unique symptoms across all records
    all_symptoms = set()
    for record in follow_up_data:
        if 'symptom_levels' in record:
            all_symptoms.update(record['symptom_levels'].keys())
    
    # Create traces for each symptom
    for symptom in all_symptoms:
        symptom_values = []
        dates = []
        
        for record in follow_up_data:
            if 'symptom_levels' in record and symptom in record['symptom_levels']:
                symptom_values.append(record['symptom_levels'][symptom])
                dates.append(record['date'])
        
        if symptom_values:  # Only add trace if there are values
            fig.add_trace(go.Scatter(
                x=dates,
                y=symptom_values,
                name=symptom.capitalize(),
                mode='lines+markers'
            ))
    
    fig.update_layout(
        title="Symptom Progression Over Time",
        xaxis_title="Date",
        yaxis_title="Severity (0-10)",
        yaxis_range=[0, 10]
    )
    
    return fig

def create_vitals_tracker_charts(follow_up_data):
    """Create line charts showing vital signs progression over time."""
    if not follow_up_data:
        return None
    
    df = pd.DataFrame(follow_up_data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Create separate figures for each vital sign
    weight_fig = go.Figure()
    temp_fig = go.Figure()
    bp_fig = go.Figure()
    
    # Weight progression
    weight_fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['weight'],
        mode='lines+markers',
        name='Weight'
    ))
    weight_fig.update_layout(
        title="Weight Progression Over Time",
        xaxis_title="Date",
        yaxis_title="Weight (kg)",
        height=300,
        yaxis=dict(range=[30, 200])
    )
    
    # Temperature progression
    temp_fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['temperature'],
        mode='lines+markers',
        name='Temperature'
    ))
    temp_fig.update_layout(
        title="Temperature Progression",
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        height=300,
        yaxis=dict(range=[35, 42])
    )
    
    # Blood Pressure progression
    systolic = []
    diastolic = []
    valid_dates = []
    
    for idx, row in df.iterrows():
        try:
            sys, dia = map(int, row['blood_pressure'].split('/'))
            systolic.append(sys)
            diastolic.append(dia)
            valid_dates.append(row['date'])
        except (ValueError, AttributeError):
            continue
    
    if valid_dates:
        bp_fig.add_trace(go.Scatter(
            x=valid_dates,
            y=systolic,
            mode='lines+markers',
            name='Systolic'
        ))
        bp_fig.add_trace(go.Scatter(
            x=valid_dates,
            y=diastolic,
            mode='lines+markers',
            name='Diastolic'
        ))
        bp_fig.update_layout(
            title="Blood Pressure Progression",
            xaxis_title="Date",
            yaxis_title="mmHg",
            height=300,
            yaxis=dict(range=[0, 200])
        )
    
    return weight_fig, temp_fig, bp_fig

def create_health_metrics_chart(follow_up_data):
    """Create a line chart showing health metrics progression over time."""
    if not follow_up_data:
        return None
    
    df = pd.DataFrame(follow_up_data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Convert string values to numeric
    metric_values = {
        'energy_level': ["Very Low", "Low", "Moderate", "Good", "Excellent"],
        'appetite': ["Poor", "Fair", "Normal", "Good", "Excellent"],
        'mobility': ["Bed-bound", "Limited", "With Assistance", "Independent", "Fully Active"],
        'sleep_quality': ["Very Poor", "Poor", "Fair", "Good", "Excellent"],
        'mood': ["Very Low", "Low", "Neutral", "Good", "Excellent"]
    }
    
    fig = go.Figure()
    
    for metric, values in metric_values.items():
        numeric_values = [values.index(val) for val in df[metric]]
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=numeric_values,
            name=metric.replace('_', ' ').title(),
            mode='lines+markers'
        ))
    
    fig.update_layout(
        title="Health Metrics Progression",
        xaxis_title="Date",
        yaxis_title="Level",
        yaxis=dict(
            ticktext=["Very Low", "Low", "Moderate", "Good", "Excellent"],
            tickvals=list(range(5))
        ),
        height=400
    )
    
    return fig

def parse_blood_pressure(bp_string):
    """Parse blood pressure string and return systolic and diastolic values."""
    try:
        sys, dia = map(int, bp_string.strip().split('/'))
        if 60 <= sys <= 200 and 40 <= dia <= 130:
            return sys, dia
        return None, None
    except (ValueError, AttributeError):
        return None, None

def patient_management_page():
    # Create consistent navigation
    create_sidebar_navigation()
    
    # Rest of your existing patient management code
    st.title("Patient Management Module")
    
    # Create tabs for different sections
    tabs = st.tabs(["Treatment Planning", "Post-Treatment Monitoring"])
    
    # Treatment Planning Tab
    with tabs[0]:
        st.header("Personalized Treatment Plan Generator")
        
        with st.form("treatment_plan_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                age = st.number_input("Age", min_value=0, max_value=120, value=50)
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
                weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
                
                cancer_type = st.selectbox(
                    "Cancer Type",
                    ["Breast", "Lung", "Prostate", "Colorectal", "Lymphoma", "Melanoma", "Leukemia", "Other"]
                )
                stage = st.selectbox(
                    "Cancer Stage",
                    ["Stage I", "Stage II", "Stage III", "Stage IV", "Unknown"]
                )
                diagnosis_date = st.date_input("Date of Diagnosis")
            
            with col2:
                current_treatment = st.multiselect(
                    "Current Treatment",
                    ["Surgery", "Chemotherapy", "Radiation", "Immunotherapy", "Hormone Therapy", "Targeted Therapy", "None"],
                    default=["None"]
                )
                
                symptoms = st.multiselect(
                    "Current Symptoms",
                    ["Pain", "Fatigue", "Nausea", "Loss of Appetite", "Breathing Difficulties", 
                     "Sleep Issues", "Anxiety/Depression", "None"],
                    default=["None"]
                )
                
                pain_level = st.slider("Pain Level (if applicable)", 0, 10, 0, help="0 = No pain, 10 = Severe pain")
                
                performance_status = st.select_slider(
                    "Performance Status",
                    options=["Fully active", "Light work possible", "Self-care only", "Limited self-care", "Completely disabled"],
                    value="Fully active",
                    help="Patient's ability to perform daily activities"
                )

            st.markdown("### Medical History")
            col3, col4 = st.columns(2)
            
            with col3:
                comorbidities = st.multiselect(
                    "Existing Medical Conditions",
                    ["Diabetes", "Hypertension", "Heart Disease", "Lung Disease", "Kidney Disease", 
                     "Liver Disease", "Autoimmune Disease", "None"],
                    default=["None"]
                )
                
                allergies = st.text_area("Allergies (if any)")
                
                smoking_status = st.radio(
                    "Smoking Status",
                    ["Never Smoked", "Former Smoker", "Current Smoker"],
                    horizontal=True
                )
            
            with col4:
                current_medications = st.text_area("Current Medications")
                family_history = st.text_area("Family History of Cancer")
                additional_notes = st.text_area("Additional Notes/Concerns")
            
            submitted = st.form_submit_button("Generate Treatment Plan")
            
            if submitted:
                patient_data = {
                    'age': age,
                    'gender': gender,
                    'cancer_type': cancer_type,
                    'stage': stage,
                    'current_treatment': current_treatment,
                    'symptoms': symptoms,
                    'medical_history': {
                        'comorbidities': comorbidities,
                        'allergies': allergies,
                        'smoking_status': smoking_status,
                        'current_medications': current_medications,
                        'family_history': family_history,
                        'additional_notes': additional_notes
                    }
                }
                
                # Store in session state
                st.session_state.patient_data = patient_data
                
                with st.spinner("Generating personalized treatment plan..."):
                    treatment_plan = generate_treatment_plan(patient_data)
                    st.markdown("### Recommended Treatment Plan")
                    st.write(treatment_plan)
                    
        # Quick Support Resources (always visible)
        st.markdown("### Quick Support Resources")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                #### Emergency Contacts
                - National Cancer Information Center: [1-800-227-2345](tel:18002272345)
                - [ACS 24/7 Live Chat](https://www.cancer.org/about-us/online-chat.html)
                - Emergency: [911](tel:911)
            """)
        
        with col2:
            st.markdown("""
                #### Support Groups & Resources
                - [American Cancer Society](https://www.cancer.org/support-programs-and-services.html)
                - [Cancer Support Community](https://www.cancersupportcommunity.org/find-support)
                - [CancerCare Support Services](https://www.cancercare.org/support_groups)
                - [National Cancer Institute Resources](https://www.cancer.gov/contact)
            """)
                    
    # Post-Treatment Monitoring Tab
    with tabs[1]:
        st.header("Post-Treatment Monitoring")
        
        # Follow-up Data Entry
        with st.form("follow_up_form"):
            st.subheader("Record Follow-up Data")
            
            col1, col2 = st.columns(2)
            
            with col1:
                date = st.date_input("Follow-up Date", datetime.now())
                weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
                blood_pressure = st.text_input("Blood Pressure (e.g., 120/80)")
                temperature = st.number_input("Temperature (°C)", min_value=35.0, max_value=42.0, value=37.0)
            
            # Symptom Severity Section
            st.markdown("### Symptom Severity")
            severity_col1, severity_col2, severity_col3 = st.columns(3)
            
            # Define all symptoms in three groups
            symptom_groups = [
                ["Pain", "Fatigue", "Nausea", "Fever", "Infection", "Bleeding"],
                ["Breathing Difficulties", "Sleep Issues", "Anxiety/Depression", "Loss of Appetite", "Diarrhea"],
                ["Constipation", "Skin Changes", "Memory Issues", "Numbness/Tingling", "Other Symptoms"]
            ]
            
            symptom_levels = {}  # Initialize dictionary for symptom levels
            
            with severity_col1:
                for symptom in symptom_groups[0]:
                    symptom_levels[symptom] = st.slider(
                        f"{symptom} Level",
                        0, 10, 0,
                        help="0 = None, 10 = Severe",
                        key=f"slider_{symptom.lower().replace('/', '_')}"
                    )

            with severity_col2:
                for symptom in symptom_groups[1]:
                    symptom_levels[symptom] = st.slider(
                        f"{symptom} Level",
                        0, 10, 0,
                        help="0 = None, 10 = Severe",
                        key=f"slider_{symptom.lower().replace('/', '_')}"
                    )

            with severity_col3:
                for symptom in symptom_groups[2]:
                    symptom_levels[symptom] = st.slider(
                        f"{symptom} Level",
                        0, 10, 0,
                        help="0 = None, 10 = Severe",
                        key=f"slider_{symptom.lower().replace('/', '_')}"
                    )

            # Additional Health Metrics
            st.markdown("### Additional Health Metrics")
            col3, col4 = st.columns(2)
            
            with col3:
                energy_level = st.select_slider(
                    "Energy Level",
                    options=["Very Low", "Low", "Moderate", "Good", "Excellent"],
                    value="Moderate"
                )
                appetite = st.select_slider(
                    "Appetite",
                    options=["Poor", "Fair", "Normal", "Good", "Excellent"],
                    value="Normal"
                )
                mobility = st.select_slider(
                    "Mobility Level",
                    options=["Bed-bound", "Limited", "With Assistance", "Independent", "Fully Active"],
                    value="Independent"
                )

            with col4:
                sleep_quality = st.select_slider(
                    "Sleep Quality",
                    options=["Very Poor", "Poor", "Fair", "Good", "Excellent"],
                    value="Fair"
                )
                mood = st.select_slider(
                    "Mood",
                    options=["Very Low", "Low", "Neutral", "Good", "Excellent"],
                    value="Neutral"
                )
                
            notes = st.text_area("Additional Notes/Observations", height=100)
            
            submitted = st.form_submit_button("Record Follow-up")
            
            if submitted:
                # Filter out symptoms with zero severity
                active_symptoms = {k: v for k, v in symptom_levels.items() if v > 0}
                
                follow_up_record = {
                    'date': date,
                    'weight': weight,
                    'blood_pressure': blood_pressure,
                    'temperature': temperature,
                    'symptom_levels': active_symptoms,
                    'energy_level': energy_level,
                    'appetite': appetite,
                    'mobility': mobility,
                    'sleep_quality': sleep_quality,
                    'mood': mood,
                    'notes': notes
                }
                st.session_state.follow_up_data.append(follow_up_record)
                st.success("Follow-up data recorded successfully!")
        
        # Display Progression Charts
        if st.session_state.follow_up_data:
            # Vital Signs Charts
            st.subheader("Vital Signs Progression")
            weight_fig, temp_fig, bp_fig = create_vitals_tracker_charts(st.session_state.follow_up_data)
            
            if weight_fig and temp_fig and bp_fig:
                st.plotly_chart(weight_fig, use_container_width=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(temp_fig, use_container_width=True)
                with col2:
                    st.plotly_chart(bp_fig, use_container_width=True)
            
            # Symptom Progression
            st.subheader("Symptom Progression")
            symptom_fig = create_symptom_tracker_chart(st.session_state.follow_up_data)
            if symptom_fig:
                st.plotly_chart(symptom_fig)
            
            # Health Metrics Progression
            st.subheader("Health Metrics Progression")
            metrics_fig = create_health_metrics_chart(st.session_state.follow_up_data)
            if metrics_fig:
                st.plotly_chart(metrics_fig)
        
        # Reminder Setup
        st.subheader("Follow-up Reminders")
        with st.form("reminder_form"):
            reminder_date = st.date_input(
                "Next Follow-up Date",
                datetime.now() + timedelta(days=30)
            )
            reminder_note = st.text_input("Reminder Note")
            
            if st.form_submit_button("Set Reminder"):
                st.session_state.reminders.append({
                    'date': reminder_date,
                    'note': reminder_note
                })
                st.success("Reminder set successfully!")
        
        # Display Reminders
        if st.session_state.reminders:
            st.markdown("### Upcoming Follow-ups")
            for reminder in st.session_state.reminders:
                st.info(f"Date: {reminder['date'].strftime('%Y-%m-%d')} - {reminder['note']}")
    
    # # Support Services Tab
    # with tabs[2]:
    #     st.header("Patient Support Services")
    #     
    #     # Current Symptoms and Concerns
    #     current_symptoms = st.multiselect(
    #         "Current Symptoms and Side Effects",
    #         ["Pain", "Fatigue", "Nausea", "Anxiety", "Depression", "Sleep Issues", "None"],
    #         default=["None"]
    #     )
    #     
    #     if st.button("Get Support Recommendations"):
    #         with st.spinner("Generating support recommendations..."):
    #             support_recommendations = generate_support_recommendations(
    #                 st.session_state.get('patient_data', {}),
    #                 current_symptoms
    #             )
    #             st.markdown("### Recommended Support Strategies")
    #             st.write(support_recommendations)
    #     
    #     # Quick Support Resources
    #     st.markdown("### Quick Support Resources")
    #     col1, col2 = st.columns(2)
    #     
    #     with col1:
    #         st.markdown('''
    #             #### Emergency Contacts
    #             - Oncology Nurse: 1-800-XXX-XXXX
    #             - 24/7 Support Line: 1-800-XXX-XXXX
    #             - Emergency: 911
    #         ''')
    #     
    #     with col2:
    #         st.markdown('''
    #             #### Support Groups
    #             - Local Cancer Support Group
    #             - Online Community Forum
    #             - Caregiver Support Network
    #         ''')

if __name__ == "__main__":
    patient_management_page()