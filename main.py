from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
from PIL import Image
import os
import re

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

def clean_filename(caption):
    # Remove special characters and replace spaces with underscores
    clean_name = re.sub(r'[^\w\s-]', '', caption)
    clean_name = clean_name.strip().replace(' ', '_')
    return clean_name

def generate_caption(image):
    inputs = processor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(**inputs)
        caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption

def process_wallpapers_folder():
    wallpapers_dir = "wallpapers"
    
    # Create wallpapers directory if it doesn't exist
    if not os.path.exists(wallpapers_dir):
        print(f"Creating {wallpapers_dir} directory...")
        os.makedirs(wallpapers_dir)
        return
    
    # Get list of image files
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    image_files = [f for f in os.listdir(wallpapers_dir) 
                   if f.lower().endswith(image_extensions)]
    
    print(f"Found {len(image_files)} images in {wallpapers_dir} directory")
    
    for filename in image_files:
        file_path = os.path.join(wallpapers_dir, filename)
        try:
            # Open and process image
            image = Image.open(file_path)
            caption = generate_caption(image)
            
            # Generate new filename
            extension = os.path.splitext(filename)[1]
            new_filename = clean_filename(caption) + extension
            new_file_path = os.path.join(wallpapers_dir, new_filename)
            
            # Rename file
            if file_path != new_file_path:
                os.rename(file_path, new_file_path)
                print(f"Renamed: {filename} -> {new_filename}")
            else:
                print(f"Skipped: {filename} (name already matches caption)")
                
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    print("Starting wallpaper caption generation and renaming...")
    process_wallpapers_folder()
    print("Processing complete!")

