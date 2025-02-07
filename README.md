# BLIP Image Captioning and Renaming Tool for Wallpaper Filenames

Rename your wallpaper images based on their content using the BLIP model.
Makes it easier to search through your wallpaper collection.

## Before & After Example

### Before:
```
wallpapers/
├── IMG_20240315_123456.jpg
├── screenshot2024-01-01.png
├── dc7x9q2-f0f2d2b9-3e12-4f61-9c1e-79a186cf5d12.jpg
├── desktop-background01.jpg
├── DSC_0042.JPG
├── wallpaper(3).png
├── download_1234.jpeg
├── New Image 12.png
├── 45692_1080p.jpg
├── untitled-1.png
... (and many more generic filenames)
```

These filenames are:
- Often generic or random (`dc7x9q2-f0f2d2b9-3e12-4f61-9c1e-79a186cf5d12.jpg`)
- Sometimes inconsistent in naming (`DSC_0042.JPG` vs `New Image 12.png`)
- Include timestamps and numbers (`IMG_20240315_123456.jpg`)
- Use inconsistent separators (spaces, underscores, hyphens)
- Don't describe the actual content at all
- Hard to search through

### After:
```
renamed/
├── a_brightly_colored_sunset_in_a_mountain_valley_with_trees_and_birds.png
├── anime_cityscape_with_a_sunset_in_the_background.png
├── anime_girl_in_a_black_coat_holding_a_umbrella_in_a_building.jpg
├── anime_girl_in_a_dress_under_the_water.jpg
├── anime_girl_in_a_long_dress_flying_through_the_air.jpg
... (and more descriptively named files)
```

The AI-generated filenames now:
- Describe the image content in detail
- Use consistent naming patterns
- Are easily searchable
- Maintain proper formatting for filenames (using underscores)

## Setup

This project uses Nix for environment management, ensuring consistent dependencies. Follow these steps to set up the environment:

1. **Install Nix:** If you don't have Nix installed, follow the instructions for your operating system at [https://nixos.org/download.html](https://nixos.org/download.html).

2. **Clone the repository:** Clone the repository containing the `flake.nix` and `main.py` files.

3. **Enter the development shell:** Navigate to the project directory in your terminal and run:

   ```bash
   nix develop
   ```

   This command will create a development environment with all the necessary dependencies (PyTorch, TorchVision, Transformers, Gradio, Python 3.12) installed.  You will be placed inside a shell where these dependencies are available.

## Usage

After entering the development shell (using `nix develop`), you can run the script using the following command:

```bash
python main.py <input_path> [-o <output_path>] [--in-place] [--device <device>]
```

**Arguments:**

*   `<input_path>`:  Required. Path to the input folder containing the wallpaper images.
*   `-o`, `--output-path`: Optional. Path to the output folder where renamed images will be saved. If not provided and `--in-place` is not used, an error will be raised.
*   `--in-place`: Optional.  If used, images will be renamed in the input folder directly.  Cannot be used with `-o` or `--output-path`.
*   `--device`: Optional. Specify the device to use for processing. Can be `cpu` or `gpu`. Defaults to `gpu` if available, otherwise falls back to `cpu`.

**Examples:**

1.  **Rename wallpapers in place:**

    ```bash
    python main.py wallpapers --in-place
    ```

2.  **Rename wallpapers and save to a new directory:**

    ```bash
    python main.py wallpapers -o renamed_wallpapers
    ```

3.  **Use CPU for processing:**

    ```bash
    python main.py wallpapers -o renamed_wallpapers --device cpu
    ```

**Important Notes:**

*   The script supports image files with extensions `.jpg`, `.jpeg`, `.png`, and `.webp`.
*   The script cleans the generated captions before using them as filenames by removing special characters and replacing spaces with underscores.
*   The script handles potential errors during image processing and provides informative messages.
*   You can interrupt the process using Ctrl+C. The script will attempt to clean up before exiting.
*   The BLIP model requires significant memory, especially for large images. Using a GPU is recommended for faster processing. If you encounter out-of-memory errors, try using the `--device cpu` option or processing images in smaller batches.

## Project Files

*   `flake.nix`: Defines the Nix development environment.
*   `main.py`: The Python script for image captioning and renaming.

This tool simplifies the process of generating captions for wallpaper images and organizing them based on their content.  It provides a convenient way to automate image tagging and management, making it easier to find the perfect wallpaper.
```
