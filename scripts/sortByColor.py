import os
import cv2
import numpy as np
from collections import Counter
import shutil

def analyze_image(image_path):
    """Analyzes image using multiple metrics to determine if it's black or white."""
    # Read image and convert to grayscale
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate basic statistics
    mean_val = np.mean(gray)
    median_val = np.median(gray)
    std_dev = np.std(gray)
    
    # Calculate histogram
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist = hist.flatten() / (gray.shape[0] * gray.shape[1])  # Normalize
    
    # Calculate percentage of very dark and very bright pixels
    dark_pixels = np.sum(gray < 20) / gray.size * 100
    bright_pixels = np.sum(gray > 235) / gray.size * 100
    
    # Check for peaks at extremes of histogram
    dark_peak = np.max(hist[:20])
    bright_peak = np.max(hist[-20:])
    
    return {
        'mean': mean_val,
        'median': median_val,
        'std_dev': std_dev,
        'dark_pixels': dark_pixels,
        'bright_pixels': bright_pixels,
        'dark_peak': dark_peak,
        'bright_peak': bright_peak
    }

def classify_image(image_path):
    """Classifies an image into Black, White, or Other using more lenient metrics."""
    stats = analyze_image(image_path)
    
    # More lenient criteria for black images
    is_black = (
        stats['mean'] < 50 and           # Was 30
        stats['median'] < 45 and         # Was 25
        stats['dark_pixels'] > 60 and    # Was 80
        stats['dark_peak'] > 0.05 and    # Was 0.1
        stats['std_dev'] < 40            # Was 25
    )
    
    # More lenient criteria for white images
    is_white = (
        stats['mean'] > 200 and          # Was 225
        stats['median'] > 195 and        # Was 230
        stats['bright_pixels'] > 60 and  # Was 80
        stats['bright_peak'] > 0.05 and  # Was 0.1
        stats['std_dev'] < 40            # Was 25
    )
    
    if is_black:
        return "Black"
    elif is_white:
        return "White"
    else:
        return "Other"

def sort_images(input_folder, output_folder):
    """Copies images into Black, White, or Other folders."""
    categories = ["Black", "White", "Other"]
    for category in categories:
        os.makedirs(os.path.join(output_folder, category), exist_ok=True)
    
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(('png', 'jpg', 'jpeg')):
            image_path = os.path.join(input_folder, file_name)
            category = classify_image(image_path)
            shutil.copy2(image_path, os.path.join(output_folder, category, file_name))
            print(f"Copied {file_name} to {category} folder")

if __name__ == "__main__":
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Get parent directory of scripts folder
    parent_dir = os.path.dirname(script_dir)
    
    # Construct absolute paths
    input_folder = os.path.join(parent_dir, "InstaAutomation", "KadhalThinamThinamInsta")
    output_folder = os.path.join(parent_dir, "InstaAutomation", "KadhalThinamThinamInsta")
    
    # Ensure input folder exists
    if not os.path.exists(input_folder):
        print(f"Error: Input folder not found: {input_folder}")
        exit(1)
        
    sort_images(input_folder, output_folder)
    print("Sorting complete!")
