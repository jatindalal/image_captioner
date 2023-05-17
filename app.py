import streamlit as st
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'

@st.cache_resource
def load_captioning_model():
    processor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
    model = AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco").to(device)

    return model, processor

def generate_captions(_image, _model, _processor, num_beams=1):
    """
    Takes in a pillow image, the captioning model and its preprocessor
    and returns a caption
    """
    pixel_values = _processor(images=_image, return_tensors="pt").to(device).pixel_values
        
    generated_ids = _model.generate(pixel_values=pixel_values, max_length=100, num_beams=num_beams)
    generated_caption = _processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_caption
    

model, preprocessor = load_captioning_model()

st.title("Generate Image Captions")

uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "png"])

num_beams = st.slider("Set the number of beams (1: Greedy Decoding) * Increasing this increases generation time...", min_value=1, max_value=5, value=1)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

    with col2:
        st.image(uploaded_file)

    with col3:
        st.write(' ')

    generated_caption = generate_captions(image, model, preprocessor, num_beams)
    st.write(f"Generated Caption: \"{generated_caption}\"")
