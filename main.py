from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
from PIL import Image
import os
import re
import argparse
import shutil
import sys

# Load BLIP processor and model
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-large"
)
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-large"
)

# Remove these lines since we'll set device after parsing args
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model = model.to(device)
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

def process_folder(input_path, output_path=None, in_place=False):
    if not os.path.exists(input_path):
        print(f"Error: Input path '{input_path}' does not exist!")
        return

    # If in_place is True, set output_path to input_path
    if in_place:
        output_path = input_path
    
    # Create output directory if it doesn't exist
    if output_path and not os.path.exists(output_path):
        print(f"Creating output directory: {output_path}")
        os.makedirs(output_path)
    
    # Get list of image files
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    image_files = [f for f in os.listdir(input_path) 
                   if f.lower().endswith(image_extensions)]
    
    print(f"Found {len(image_files)} images in {input_path}")
    
    try:
        for filename in image_files:
            input_file_path = os.path.join(input_path, filename)
            try:
                # Open and process image
                image = Image.open(input_file_path)
                caption = generate_caption(image)
                
                # Generate new filename
                extension = os.path.splitext(filename)[1]
                new_filename = clean_filename(caption) + extension
                
                if output_path:
                    new_file_path = os.path.join(output_path, new_filename)
                    if not in_place:
                        # Copy to new location with new name
                        shutil.copy2(input_file_path, new_file_path)
                        print(f"Copied and renamed: {filename} -> {new_filename}")
                    else:
                        # Rename in place
                        if input_file_path != new_file_path:
                            os.rename(input_file_path, new_file_path)
                            print(f"Renamed: {filename} -> {new_filename}")
                        else:
                            print(f"Skipped: {filename} (name already matches caption)")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Cleaning up...")
        return

def main():
    parser = argparse.ArgumentParser(description='Generate captions for images and rename/move them accordingly.')
    parser.add_argument('input_path', help='Path to the input folder containing images')
    parser.add_argument('-o', '--output-path', help='Path to the output folder (optional)')
    parser.add_argument('--in-place', action='store_true', 
                        help='Rename files in the input folder instead of copying to output')
    parser.add_argument('--device', choices=['cpu', 'gpu'], default='gpu',
                        help='Device to use for processing (default: gpu if available, else cpu)')
    
    try:
        args = parser.parse_args()
        
        # Set device based on argument or availability
        global device
        if args.device == 'gpu':
            if torch.cuda.is_available():
                device = torch.device('cuda')
            else:
                print("Warning: GPU requested but not available. Using CPU instead.")
                device = torch.device('cpu')
        else:
            device = torch.device('cpu')
        
        # Move model to selected device
        global model
        model = model.to(device)
        
        if args.in_place and args.output_path:
            print("Error: Cannot use both --in-place and --output-path")
            return
        
        if not args.in_place and not args.output_path:
            print("Error: Must specify either --output-path or --in-place")
            return
        
        print(f"Using device: {device}")
        print("Starting image caption generation and processing...")
        process_folder(args.input_path, args.output_path, args.in_place)
        print("Processing complete!")
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
        sys.exit(1)

if __name__ == "__main__":
    main()

