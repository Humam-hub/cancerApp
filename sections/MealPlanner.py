import streamlit as st
from utils import initialize_groq_client, get_ai_response, create_sidebar_navigation

def generate_meal_plan(preferences):
    """
    Generate a cancer-friendly meal plan using Groq API.
    
    Args:
        preferences (dict): Dictionary containing user dietary preferences
    
    Returns:
        str: Generated meal plan and grocery list
    """
    client = initialize_groq_client()
    if not client:
        return "Error: Unable to initialize AI client"

    # Format dietary restrictions
    restrictions = ', '.join(preferences['allergies']) if preferences['allergies'] else 'None'
    diet_type = ', '.join(preferences['diet_type']) if preferences['diet_type'] else 'Regular'

    prompt = f"""
    Create a 7-day cancer-friendly meal plan and grocery list with these specifications:
    - Dietary Restrictions: {restrictions}
    - Diet Type: {diet_type}
    - Budget Level: {preferences['budget']}
    - Taste Preferences: {preferences['taste_preferences']}
    
    The meal plan should:
    1. Focus on cancer-fighting foods and nutrients
    2. Include breakfast, lunch, dinner, and two snacks for each day
    3. Provide portion sizes and basic preparation instructions
    4. Consider the specified budget level
    5. Include foods known for their anti-inflammatory properties
    
    Also generate a comprehensive grocery list organized by:
    1. Produce (fruits and vegetables)
    2. Proteins
    3. Grains and starches
    4. Pantry items
    5. Herbs and spices
    
    Format the response clearly with section headers and daily breakdowns.
    """
    
    return get_ai_response(client, prompt)

def meal_planner_page():
    # Create consistent navigation
    create_sidebar_navigation()
    
    st.title("🥗 Cancer-Friendly Meal Planner")
    
    st.markdown("""
    ### Plan Your Nutritious Week
    Get a personalized, cancer-friendly meal plan based on your preferences and dietary needs. 
    Our AI considers the latest nutritional research for cancer prevention and recovery.
    """)
    
    # Initialize meal_plan outside the form
    meal_plan = None
    
    # User Preferences Form
    with st.form("meal_preferences_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            allergies = st.multiselect(
                "Dietary Restrictions & Allergies",
                ["Gluten", "Dairy", "Nuts", "Soy", "Eggs", "Shellfish", "Fish"],
                default=None,
                help="Select any foods you need to avoid"
            )
            
            diet_type = st.multiselect(
                "Diet Type",
                ["Vegetarian", "Vegan", "Pescatarian", "Mediterranean", "Regular"],
                default=["Regular"],
                help="Select your preferred diet type"
            )
            
            budget = st.select_slider(
                "Budget Level",
                options=["Low", "Medium", "High"],
                value="Medium",
                help="Select your preferred budget level"
            )
        
        with col2:
            taste_preferences = st.multiselect(
                "Taste Preferences",
                ["Mild", "Spicy", "Sweet", "Savory", "All"],
                default=["All"],
                help="Select your taste preferences"
            )
            
            st.markdown("### Additional Preferences")
            batch_cooking = st.checkbox("Include batch cooking options", value=True)
            easy_prep = st.checkbox("Focus on easy-to-prepare meals", value=True)
            leftovers = st.checkbox("Plan for leftovers", value=True)
        
        submitted = st.form_submit_button("Generate Meal Plan")
        
        if submitted:
            preferences = {
                'allergies': allergies,
                'diet_type': diet_type,
                'budget': budget,
                'taste_preferences': taste_preferences,
                'batch_cooking': batch_cooking,
                'easy_prep': easy_prep,
                'leftovers': leftovers
            }
            
            with st.spinner("Creating your personalized meal plan..."):
                meal_plan = generate_meal_plan(preferences)
    
    # Move meal plan display and download button outside the form
    if meal_plan:
        if "Error" in meal_plan:
            st.error(meal_plan)
        else:
            # Display the meal plan in an expandable container
            with st.expander("📅 Your 7-Day Meal Plan", expanded=True):
                st.markdown(meal_plan)
            
            # Add download button for the meal plan
            st.download_button(
                label="Download Meal Plan",
                data=meal_plan,
                file_name="cancer_friendly_meal_plan.txt",
                mime="text/plain"
            )

    # Nutritional Guidelines Section
    with st.expander("ℹ️ Cancer-Fighting Nutrition Guidelines"):
        st.markdown("""
        ### Key Nutritional Guidelines for Cancer Prevention
        
        1. **Eat the Rainbow 🌈**
           - Dark leafy greens (spinach, kale)
           - Colorful vegetables and fruits
           - Berries and citrus fruits
        
        2. **Protein Sources 🥜**
           - Lean poultry
           - Fish rich in omega-3
           - Plant-based proteins
        
        3. **Healthy Fats 🥑**
           - Avocados
           - Olive oil
           - Nuts and seeds
        
        4. **Foods to Limit ⚠️**
           - Processed meats
           - Excessive red meat
           - Refined sugars
           - Alcohol
        """)
    
    # Tips for Food Preparation
    with st.expander("🔍 Food Preparation Tips"):
        st.markdown("""
        ### Safe Food Preparation During Cancer Treatment
        
        1. **Cleaning 🧼**
           - Wash all produce thoroughly
           - Clean preparation surfaces
           - Use separate cutting boards
        
        2. **Storage 🌡️**
           - Keep food at safe temperatures
           - Store leftovers properly
           - Use airtight containers
        
        3. **Cooking 👩‍🍳**
           - Cook foods thoroughly
           - Avoid raw or undercooked items
           - Use food thermometer when needed
        """)

if __name__ == "__main__":
    meal_planner_page() 