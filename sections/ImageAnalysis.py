import streamlit as st
from utils import create_sidebar_navigation
from gradio_client import Client
import tempfile
import json
import os

def image_analysis_page():
    # Create consistent navigation
    create_sidebar_navigation()

    st.title("🔬 Breast Cancer Classification")
    st.markdown("""
    ### Upload a histopathological image for breast cancer classification
    This tool analyzes microscopic images of breast tissue to assist in cancer detection.
    """)

    # File uploader widget for image input
    uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        
        try:
            # Save the uploaded file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name

            # Button to trigger prediction
            if st.button("Get Prediction"):
                with st.spinner("Analyzing image..."):
                    try:
                        # Create a Gradio client pointing to the remote endpoint
                        client = Client("https://hasanah10105-breast-cancer-classification.hf.space/--replicas/12gx2/")
                        
                        # Get prediction
                        result = client.predict(tmp_file_path, fn_index=0)
                        
                        # Parse and display results
                        if isinstance(result, str):
                            try:
                                # Read the JSON file that was returned
                                with open(result, 'r') as json_file:
                                    result_dict = json.load(json_file)
                                    st.success("Analysis Complete!")
                                    
                                    # Display prediction results in a formatted way
                                    st.markdown("### Analysis Results")
                                    for key, value in result_dict.items():
                                        if isinstance(value, (int, float)):
                                            # Format numbers to 2 decimal places
                                            st.metric(key.replace('_', ' ').title(), f"{value:.2f}")
                                        else:
                                            st.metric(key.replace('_', ' ').title(), value)
                            except (json.JSONDecodeError, FileNotFoundError) as e:
                                st.error(f"Error reading prediction results: {e}")
                                st.write("Raw result:", result)
                        else:
                            st.write("Prediction Result:", result)
                            
                    except Exception as e:
                        st.error(f"An error occurred during prediction: {e}")
        except Exception as e:
            st.error(f"An error occurred while processing the image: {e}")
        finally:
            # Cleanup temporary file
            if 'tmp_file_path' in locals():
                try:
                    os.unlink(tmp_file_path)
                except Exception as e:
                    st.warning(f"Could not delete temporary file: {e}")

if __name__ == "__main__":
    image_analysis_page()