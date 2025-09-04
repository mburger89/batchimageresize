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
def batch_resize(input_folder, output_folder=None, target_size=(1024, 1024) ):
	"""
	Resize all images in a folder from 2048x2048 to 1024x1024

	Args:
		input_folder (str): Path to folder containing images
		output_folder (str): Path to output folder (creates if doesn't exist)
		extensions (tuple): Tuple of valid image extensions
	"""
	if output_folder is None:
		output_folder = os.path.join(input_folder, "resized")
	# Create output folder if it doesn't exist
	os.makedirs(output_folder, exist_ok=True)
	# Process all images in the folder
	processed = 0
	for filename in os.listdir(input_folder):
		print(filename)
		if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
			input_path = os.path.join(input_folder, filename)
			output_path = os.path.join(output_folder, filename)

			print(f"\nProcessing: {filename}")
			if resize_image(input_path, output_path, target_size):
				processed += 1

	print(f"\n{'='*50}")
	print(f"Batch processing complete! Processed {processed} images.")
	print(f"Output folder: {output_folder}")
	return True

def HelpInfo():
	print("Usage: python resize_image.py <input_image> [output_image]")
	print("Example: python resize_image.py image_2048.png image_1024.png")
	print("Flags:")
	print("  -f <folder_path>: Path to folder of folders containing images to resize")
	print("  -t <width> <height>: Target size for resizing")
	print("Help: python resize_image.py -h")

def main():
	"""
	Main function to handle command line arguments
	Args:
		input_folder (str): Path to input folder
		output_folder (str): Path to output folder (creates if doesn't exist)
		flags (str): Flags for additional processing (-f to process a folder of folders of images)
	"""
	extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
	flag = ""
	mvOGPath = ""
	target_size = (1024, 1024)
	# Check command line arguments
	if len(sys.argv) < 2:
		HelpInfo()
		sys.exit(1)
	elif sys.argv[1] == "-h":
		HelpInfo()
		sys.exit(1)

	if "-t" in sys.argv:
		target_size = (int(sys.argv[sys.argv.index("-t") + 1]), int(sys.argv[sys.argv.index("-t") + 2]))

	if '-p' in sys.argv:
		mvOGPath = sys.argv[sys.argv.index('-p') + 1]

	if len(sys.argv) == 3:
		flag = sys.argv[1]
		input_file = sys.argv[2]
		output_file = sys.argv[3] if len(sys.argv) > 3 else None
	else:
		input_file = sys.argv[1]
		output_file = sys.argv[2] if len(sys.argv) > 2 else None

	# Perform the resize
	success = False
	# if its only one file resize it
	if input_file.split('.')[-1] in ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff']:
		success = resize_image(input_file, output_file, target_size)
	# if the flag is set read the files in the folders and resize them
	elif flag == '-f':
		folders = os.listdir(input_file)
		for f in folders:
			# create folders for each version and file type
			os.makedirs(os.path.join(input_file, f,"USD"), exist_ok=True)
			os.makedirs(os.path.join(input_file, f,f"Original_{f}"), exist_ok=True)
			os.makedirs(os.path.join(input_file, f,"1k"), exist_ok=True)
			# move files to each version folder
			for file in os.listdir(os.path.join(input_file, f)):
				if file.endswith(extensions):
					move(os.path.join(input_file, f, file), os.path.join(input_file, f,f"Original_{f}", file))
				if file.endswith((".usda", ".usdc", ".usdz")):
					move(os.path.join(input_file, f, file), os.path.join(input_file, f,"USD", file))
			# resize images in the Original folder and write them to the 1k folder
			success = batch_resize(os.path.join(input_file, f, f"Original_{f}"), os.path.join(input_file, f, "1k"), target_size)
	elif flag == '-rcp':
		folders = os.listdir(input_file)
		for f in folders:
			os.makedirs(os.path.join(input_file, f,f"original_{f}"), exist_ok=True)
			for file in os.listdir(os.path.join(input_file, f)):
				if file.endswith(extensions):
					move(os.path.join(input_file, f, file), os.path.join(input_file, f,f"original_{f}", file))
			success = batch_resize(os.path.join(input_file, f, f"original_{f}"), os.path.join(input_file, f), target_size)
			move(os.path.join(input_file, f, f"original_{f}"), mvOGPath)
	elif len(os.listdir(input_file)) > 0:
		success = batch_resize(input_file, output_file, target_size)
	else:
		print(f"Error: '{input_file}' is not a valid image file or folder structure")
		success = False

	if not success:
		sys.exit(1)

if __name__ == "__main__":
	main()
