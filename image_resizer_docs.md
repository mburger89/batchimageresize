# Image Resizer Script - 2048 to 1024 Converter

A Python script that efficiently resizes 2048x2048 images to 1024x1024 while maintaining high quality.

## Features

- **Simple command-line usage**: Run directly from terminal with image path
- **High-quality resizing**: Uses LANCZOS resampling for best quality
- **Automatic output naming**: Auto-generates output filename if not specified
- **Error handling**: Validates file existence and handles errors gracefully
- **Batch processing**: Resize multiple images at once
- **Format preservation**: Maintains original image format (PNG, JPEG, etc.)

## Installation

### Prerequisites

- Python 3.6 or higher
- Pillow library
<!---->
### Install Dependencies

```bash
pip install Pillow
```

## Python Script

Save the following code as `resize_image.py`:

```python
#!/usr/bin/env python3
"""
Script to resize a 2048x2048 image to 1024x1024
"""

from PIL import Image
import os
import sys


def resize_image(input_path, output_path=None, target_size=(1024, 1024)):
    """
    Resize an image to the specified dimensions.

    Args:
        input_path (str): Path to the input image
        output_path (str): Path for the output image (optional)
        target_size (tuple): Target dimensions (width, height)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Open the image
        img = Image.open(input_path)

        # Get original dimensions
        original_size = img.size
        print(f"Original image size: {original_size[0]} x {original_size[1]}")

        # Check if image is 2048x2048 (optional warning)
        if original_size != (2048, 2048):
            print(f"Warning: Input image is not 2048x2048. Proceeding with resize...")

        # Resize the image using LANCZOS resampling for high quality
        resized_img = img.resize(target_size, Image.Resampling.LANCZOS)

        # Generate output path if not provided
        if output_path is None:
            base_name = os.path.splitext(input_path)[0]
            extension = os.path.splitext(input_path)[1]
            output_path = f"{base_name}_1024x1024{extension}"

        # Save the resized image
        resized_img.save(output_path)

        print(f"Successfully resized image to {target_size[0]} x {target_size[1]}")
        print(f"Saved to: {output_path}")

        return True

    except FileNotFoundError:
        print(f"Error: Could not find the file '{input_path}'")
        return False
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")
        return False


def main():
    """
    Main function to handle command line arguments
    """
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python resize_image.py <input_image> [output_image]")
        print("Example: python resize_image.py image_2048.png image_1024.png")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    # Perform the resize
    success = resize_image(input_file, output_file)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()


# Alternative: Batch processing function for multiple images
def batch_resize(input_folder, output_folder=None, extensions=('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
    """
    Resize all images in a folder from 2048x2048 to 1024x1024

    Args:
        input_folder (str): Path to folder containing images
        output_folder (str): Path to output folder (creates if doesn't exist)
        extensions (tuple): Tuple of valid image extensions
    """
    if output_folder is None:
        output_folder = os.path.join(input_folder, "resized_1024")

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Process all images in the folder
    processed = 0
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(extensions):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            print(f"\nProcessing: {filename}")
            if resize_image(input_path, output_path):
                processed += 1

    print(f"\n{'='*50}")
    print(f"Batch processing complete! Processed {processed} images.")
    print(f"Output folder: {output_folder}")
```

## Usage Examples

### Command Line Usage

#### Basic usage (auto-generates output filename)
```bash
python resize_image.py input_image.png
```
This will create `input_image_1024x1024.png` in the same directory.

#### Specify output filename
```bash
python resize_image.py input_image.png output_image.png
```

#### Process multiple files
```bash
python resize_image.py photo1.jpg resized_photo1.jpg
python resize_image.py photo2.png resized_photo2.png
```

### Python Code Usage

#### Import and use in your Python scripts

```python
from resize_image import resize_image, batch_resize

# Single image resize
resize_image("my_2048_image.png", "my_1024_image.png")

# Auto-generate output filename
resize_image("photo.jpg")  # Creates photo_1024x1024.jpg

# Batch process entire folder
batch_resize("./images_folder", "./resized_images")

# Batch process with default output folder
batch_resize("./images_folder")  # Creates ./images_folder/resized_1024/
```

## Supported Image Formats

The script supports all common image formats:
- PNG (.png)
- JPEG (.jpg, .jpeg)
- BMP (.bmp)
- GIF (.gif)
- TIFF (.tiff, .tif)
- WebP (.webp)

## Advanced Usage

### Custom Target Size

Modify the `target_size` parameter to resize to different dimensions:

```python
# Resize to 512x512
resize_image("input.png", "output.png", target_size=(512, 512))

# Resize to 4096x4096
resize_image("input.png", "output.png", target_size=(4096, 4096))
```

### Batch Processing with Custom Extensions

```python
# Only process PNG and JPG files
batch_resize("./images", "./output", extensions=('.png', '.jpg'))
```

## Tips and Best Practices

1. **Image Quality**: The script uses LANCZOS resampling, which provides the best quality for downsizing images.

2. **File Organization**: When batch processing, the script creates a separate output folder to keep original images intact.

3. **Memory Usage**: For very large batches of images, consider processing them in chunks to manage memory usage.

4. **Aspect Ratio**: The script forces resize to 1024x1024, which may distort images that aren't square. For non-square images, consider modifying the script to maintain aspect ratio.

## Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'PIL'` | Install Pillow: `pip install Pillow` |
| `FileNotFoundError` | Check that the image path is correct and the file exists |
| `PermissionError` | Ensure you have write permissions in the output directory |
| Out of memory error | Process images in smaller batches or resize one at a time |

### Error Messages

- **"Input image is not 2048x2048"**: This is a warning only. The script will still resize the image to 1024x1024.
- **"Could not find the file"**: Verify the file path and ensure the image exists.
- **"An unexpected error occurred"**: Check file permissions and ensure the image file is not corrupted.

## Performance Notes

- Processing time depends on image complexity and system specifications
- Typical resize time: 0.1-0.5 seconds per image
- Batch processing is more efficient than individual conversions
- LANCZOS resampling is slower but produces better quality than other methods

## License

This script is provided as-is for personal and commercial use.

## Contributing

Feel free to modify and enhance the script for your specific needs. Common enhancements might include:
- Adding a GUI interface
- Supporting additional image formats
- Implementing aspect ratio preservation
- Adding image optimization features
- Creating a progress bar for batch processing
