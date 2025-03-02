import os
import cv2
import numpy as np
import shutil
from tqdm import tqdm

def rgb_to_hsv(rgb):
    """Convert RGB to HSV color space."""
    rgb_normalized = np.array([[rgb]], dtype=np.uint8)
    hsv = cv2.cvtColor(rgb_normalized, cv2.COLOR_RGB2HSV)
    return hsv[0][0]

def get_dominant_color(image_path, k=3):
    """Extracts the dominant color from an image using K-Means clustering."""
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = np.float32(image.reshape(-1, 3))
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
    _, _, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    return tuple(map(int, centers[0]))

def get_color_category(image_path):
    """Determines the dominant color category and its percentage."""
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Calculate average HSV values for sorting
    avg_h = np.mean(hsv[:,:,0])
    avg_s = np.mean(hsv[:,:,1])
    avg_v = np.mean(hsv[:,:,2])
    
    # Enhanced VIBGYOR color ranges in HSV with more precise boundaries
    color_ranges = {
        'Violet': ([135, 35, 35], [155, 255, 255]),
        'Indigo': ([120, 35, 35], [135, 255, 255]),
        'Blue':   ([100, 35, 35], [120, 255, 255]),
        'Green':  ([45, 35, 35], [90, 255, 255]),
        'Yellow': ([25, 35, 35], [45, 255, 255]),
        'Orange': ([10, 35, 35], [25, 255, 255]),
        'Red1':   ([0, 35, 35], [10, 255, 255]),
        'Red2':   ([160, 35, 35], [180, 255, 255])
    }
    
    total_pixels = hsv.shape[0] * hsv.shape[1]
    color_percentages = {}
    
    # Calculate percentages for each color
    for color, (lower, upper) in color_ranges.items():
        lower = np.array(lower)
        upper = np.array(upper)
        mask = cv2.inRange(hsv, lower, upper)
        color_pixels = np.sum(mask > 0)
        percentage = (color_pixels / total_pixels) * 100
        color_percentages[color] = percentage
    
    # Handle combined Red percentage
    if 'Red1' in color_percentages and 'Red2' in color_percentages:
        color_percentages['Red'] = color_percentages['Red1'] + color_percentages['Red2']
        del color_percentages['Red1']
        del color_percentages['Red2']
    
    # Get the dominant color
    dominant_color = max(color_percentages.items(), key=lambda x: x[1])[0]
    
    # Enhanced normalization for smoother transitions
    normalized_h = avg_h
    if dominant_color == 'Red' and avg_h > 160:
        normalized_h = 0
    
    # Weight the HSV components for better sorting
    weighted_s = avg_s * 0.7  # Reduce impact of saturation
    weighted_v = avg_v * 0.3  # Reduce impact of value
    
    return dominant_color, color_percentages[dominant_color], (normalized_h, weighted_s, weighted_v)

def clean_filename(filename):
    """Removes existing color tags from filename."""
    # Remove pattern like "dddd_Color_" from start of filename
    import re
    cleaned = re.sub(r'^\d{4}_[A-Za-z]+_', '', filename)
    return cleaned

def are_images_similar(img1_path, img2_path, threshold=0.85):
    """Compare two images and return True if they are similar."""
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    # Resize images to same size for comparison
    size = (300, 300)
    img1 = cv2.resize(img1, size)
    img2 = cv2.resize(img2, size)
    
    # Compare using histogram similarity
    hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist2 = cv2.calcHist([img2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    
    hist1 = cv2.normalize(hist1, hist1).flatten()
    hist2 = cv2.normalize(hist2, hist2).flatten()
    
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return similarity > threshold

def space_out_similar_images(images_in_color):
    """Ensure similar images are not adjacent by inserting spacing."""
    result = []
    pending_similar = []
    min_gap = 3  # Minimum number of images between similar ones
    
    for img in images_in_color:
        if not result:
            result.append(img)
            continue
            
        # Check if current image is similar to any recent images
        is_similar = False
        for prev_img in result[-min_gap:]:
            if are_images_similar(prev_img[2], img[2]):  # Compare file paths
                is_similar = True
                break
        
        if is_similar:
            pending_similar.append(img)
        else:
            result.append(img)
            # Try to insert pending similar images if enough gap exists
            while pending_similar and len(result) >= min_gap:
                can_insert = True
                candidate = pending_similar[0]
                for recent_img in result[-min_gap:]:
                    if are_images_similar(recent_img[2], candidate[2]):
                        can_insert = False
                        break
                if can_insert:
                    result.append(pending_similar.pop(0))
                else:
                    break
    
    # Append remaining pending images with maximum possible spacing
    result.extend(pending_similar)
    return result

def sort_by_spectrum(input_folder, output_folder, needWhiteOrBlack=False):
    """Sorts images by specific color order: VIBGYOR with internal color sorting."""
    os.makedirs(output_folder, exist_ok=True)
    
    # Define VIBGYOR order
    color_order = ['Violet', 'Indigo', 'Blue', 'Green', 'Yellow', 'Orange', 'Red']
    
    print("Analyzing image colors...")
    # Create a dictionary to store images by color
    color_groups = {color: [] for color in color_order}
    
    image_files = [f for f in os.listdir(input_folder) 
                   if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    
    for file_name in tqdm(image_files, desc="Analyzing colors"):
        image_path = os.path.join(input_folder, file_name)
        color, intensity, hsv = get_color_category(image_path)
        if color in color_order:  # Only process VIBGYOR colors
            color_groups[color].append((intensity, hsv, file_name))
    
    print("\nSorting color groups and spacing similar images...")
    index = 0
    for color in color_order:
        # Sort images within each color group by saturation and value
        color_group = [(intensity, hsv, os.path.join(input_folder, file_name)) 
                      for intensity, hsv, file_name in color_groups[color]]
        color_group.sort(key=lambda x: (x[1][1], x[1][2]))
        
        # Space out similar images within each color group
        spaced_group = space_out_similar_images(color_group)
        
        # Copy sorted and spaced images
        for intensity, hsv, file_path in spaced_group:
            file_name = os.path.basename(file_path)
            cleaned_name = clean_filename(file_name)
            new_name = f"{index:04d}_{color}_{cleaned_name}"
            new_path = os.path.join(output_folder, new_name)
            shutil.copy2(file_path, new_path)
            print(f"Copying {color}: {new_name}")
            index += 1

    print(f"\nColor distribution:")
    for color in color_order:
        count = len(color_groups[color])
        print(f"{color}: {count} images")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    input_folder = os.path.join(parent_dir, "InstaAutomation", "KadhalThinamThinamInsta", "Other")
    output_folder = os.path.join(parent_dir, "InstaAutomation", "KadhalThinamThinamInsta", "Spectrum")
    
    if not os.path.exists(input_folder):
        print(f"Error: Input folder not found: {input_folder}")
        exit(1)
        
    sort_by_spectrum(input_folder, output_folder, needWhiteOrBlack=False)
    print("Spectrum sorting complete!")
