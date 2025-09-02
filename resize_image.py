#!/usr/bin/env python3
"""
Script to resize a 2048x2048 image to 1024x1024
"""

from PIL import Image
import os
import sys
from shutil import move


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
			print("Warning: Input image is not 2048x2048. Proceeding with resize...")

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
	return True

def main():
	"""
	Main function to handle command line arguments
	Args:
		input_folder (str): Path to input folder
		output_folder (str): Path to output folder (creates if doesn't exist)
		flags (str): Flags for additional processing (-f to process a folder of folders of images)
	"""
	extensions=('.png', '.jpg', '.jpeg', '.bmp', '.gif')
	flag = ""
	# Check command line arguments

	if len(sys.argv) < 2:
		print("Usage: python resize_image.py <input_image> [output_image]")
		print("Example: python resize_image.py image_2048.png image_1024.png")
		sys.exit(1)
	elif sys.argv[1] == "-h":
		print("Usage: python resize_image.py <input_image> [output_image]")
		print("Example: python resize_image.py image_2048.png image_1024.png")
		print("Flags: -f to process a folder of folders of images")
		print("Help: python resize_image.py -h")
		sys.exit(1)

	if len(sys.argv) == 3:
		flag = sys.argv[1]
		input_file = sys.argv[2]
		output_file = sys.argv[3] if len(sys.argv) > 3 else None
	else:
		input_file = sys.argv[1]
		output_file = sys.argv[2] if len(sys.argv) > 2 else None

	# Perform the resize
	success = False

	if input_file.split('.')[-1] in ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff']:
		success = resize_image(input_file, output_file)
	elif flag == '-f':
		folders = os.listdir(input_file)
		for f in folders:
			os.makedirs(os.path.join(input_file, f,"USD"), exist_ok=True)
			os.makedirs(os.path.join(input_file, f,"2K"), exist_ok=True)
			os.makedirs(os.path.join(input_file, f,"1k"), exist_ok=True)
			for file in os.listdir(os.path.join(input_file, f)):
				if file.endswith(extensions):
					move(os.path.join(input_file, f, file), os.path.join(input_file, f,"2K", file))
				if file.endswith((".usda", ".usdc", ".usdz")):
					move(os.path.join(input_file, f, file), os.path.join(input_file, f,"USD", file))
			success = batch_resize(os.path.join(input_file, f, "2K"), os.path.join(input_file, f, "1k"))
	elif len(os.listdir(input_file)) > 0:
		success = batch_resize(input_file, output_file)
	else:
		print(f"Error: '{input_file}' is not a valid image file")
		success = False

	if not success:
		sys.exit(1)


if __name__ == "__main__":
	main()
