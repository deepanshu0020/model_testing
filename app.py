import streamlit as st
from PIL import Image
import os
from os.path import join, dirname, realpath
import matplotlib.pyplot as plt 

from pipeline import pipeline 

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')
ALLOWED_EXTENSIONS = {'png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'gif', 'GIF'}

# Create the uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

st.title("Image Assessment App")

uploaded_file = st.file_uploader("Choose an image...", type=ALLOWED_EXTENSIONS)

if uploaded_file is not None:
    # Save the uploaded file
    filename = uploaded_file.name
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display the uploaded image
    st.image(Image.open(uploaded_file), caption='Uploaded Image', use_column_width=True)

    # Run the pipeline
    if st.button("Assess"):
        with st.spinner("Assessing..."):
            model_results, model_accuracies = pipeline.pipe(filepath) 

        # Display the results
        st.write("## Assessment Results")
        st.write(model_results)  

        # Display model accuracies
        st.write("## Model Accuracies")

        # Create a bar chart
        fig, ax = plt.subplots()
        model_names = list(model_accuracies.keys())
        accuracies = list(model_accuracies.values())
        ax.bar(model_names, accuracies)
        ax.set_ylabel("Accuracy")
        ax.set_title("Accuracy of Models")

        # Display the chart in Streamlit
        st.pyplot(fig)
