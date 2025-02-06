from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
from PIL import Image
import gradio as gr

# Load BLIP processor and model
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-large"
)
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-large"
)

# Define the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Move the model to the device
model = model.to(device)
model.eval()  # Set the model to evaluation mode


def generate_caption(image):
    text = "wallpaper of"
    inputs = processor(images=image, return_tensors="pt").to(
        device
    )  # Move inputs to the device

    with torch.no_grad():  # Disable gradient calculation for inference
        outputs = model.generate(**inputs)
        caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption


# Create Gradio interface
iface = gr.Interface(
    fn=generate_caption,
    inputs=gr.Image(type="pil"),
    outputs="text",
    title="Image Captioning with BLIP",
    description="Generate captions for your images using the BLIP model.",
)

# Launch the interface
iface.launch()

