import streamlit as st
from PIL import Image
from google.cloud import vision
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import io
from dotenv import load_dotenv
import os

load_dotenv()
service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'trueinfolabs-ocr-20c8c095084b.json'

client = vision.ImageAnnotatorClient() 

def extract_text_with_google_vision_api(image):
    """Extract text from image using Google Cloud Vision API."""

    # Convert PIL image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format)
    image_bytes = img_byte_arr.getvalue()

    # Prepare the image for Google Vision API
    image = vision.Image(content=image_bytes)

    # Detect text in the image
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Extract the first text annotation which contains the entire extracted text
    if texts:
        return texts[0].description
    else:
        return "No text found."

def main():

    st.title("Text Extraction from Image in English and Tamil using Google Cloud Vision API")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        text = extract_text_with_google_vision_api(image)

        st.success("Text extracted successfully!")
        st.header("Extracted Text:")
        st.write(text)

if __name__ == "__main__":
    main()