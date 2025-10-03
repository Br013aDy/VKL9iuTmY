# 代码生成时间: 2025-10-04 01:40:21
import os
from celery import Celery
from PIL import Image, ImageFilter

# Celery configuration
app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def apply_filter(image_path, filter_type):
    '''
    Applies a specified filter to an image.
    
    Parameters:
    - image_path (str): Path to the image file.
    - filter_type (str): Type of filter to apply.
    
    Returns:
    - str: Path to the filtered image file.
    
    Raises:
    - FileNotFoundError: If the image file does not exist.
    - ValueError: If the filter type is not supported.
    '''
    # Supported filters
    supported_filters = {
        'BLUR': ImageFilter.BLUR,
        'CONTOUR': ImageFilter.CONTOUR,
        'DETAIL': ImageFilter.DETAIL,
        'EDGE_ENHANCE': ImageFilter.EDGE_ENHANCE,
        'SHARPEN': ImageFilter.SHARPEN,
        'SMOOTH': ImageFilter.SMOOTH
    }

    # Check if the filter type is supported
    if filter_type not in supported_filters:
        raise ValueError(f"Unsupported filter type: {filter_type}")

    # Check if the image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Open the image and apply the filter
    try:
        with Image.open(image_path) as img:
            filtered_img = img.filter(supported_filters[filter_type])
            # Save the filtered image
            filtered_image_path = f"{os.path.splitext(image_path)[0]}_filtered{os.path.splitext(image_path)[1]}"
            filtered_img.save(filtered_image_path)
            return filtered_image_path
    except IOError as e:
        # Handle image read/write errors
        raise IOError(f"Error reading or writing image: {e}")
