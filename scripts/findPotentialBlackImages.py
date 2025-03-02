import os
import cv2
import numpy as np
from tqdm import tqdm

def analyze_dark_potential(image_path):
    """Analyzes an image to determine if it could make a good black image."""
    # Read image and convert to different color spaces
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Calculate various metrics
    metrics = {
        'mean_brightness': np.mean(gray),
        'median_brightness': np.median(gray),
        'dark_pixel_percentage': np.sum(gray < 50) / gray.size * 100,
        'very_dark_pixel_percentage': np.sum(gray < 30) / gray.size * 100,
        'brightness_std': np.std(gray),
        'value_mean': np.mean(hsv[:,:,2]),
        'saturation_mean': np.mean(hsv[:,:,1])
    }
    
    # Calculate histogram features
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist = hist.flatten() / gray.size
    metrics['dark_peak'] = np.max(hist[:50])
    metrics['bright_peak'] = np.max(hist[200:])
    
    # Calculate potential score (0-100)
    score = 0
    
    # Score based on brightness (want it relatively dark but not too dark)
    if 40 < metrics['mean_brightness'] < 80:
        score += 30
    elif 30 < metrics['mean_brightness'] < 90:
        score += 20
    
    # Score based on dark pixel percentage
    if metrics['dark_pixel_percentage'] > 60:
        score += 20
    elif metrics['dark_pixel_percentage'] > 40:
        score += 10
    
    # Score based on contrast (want some variation for interesting blacks)
    if 10 < metrics['brightness_std'] < 30:
        score += 20
    elif 5 < metrics['brightness_std'] < 40:
        score += 10
    
    # Score based on saturation (lower is better for black conversion)
    if metrics['saturation_mean'] < 50:
        score += 15
    elif metrics['saturation_mean'] < 80:
        score += 5
    
    # Score based on histogram distribution
    if metrics['dark_peak'] > 0.1 and metrics['bright_peak'] < 0.05:
        score += 15
    
    return score, metrics

def find_potential_black_images(folder_path, threshold=70):
    """Finds images that could potentially be converted to good black images."""
    candidates = []
    
    image_files = [f for f in os.listdir(folder_path) 
                   if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    
    print("Analyzing images for black potential...")
    for file_name in tqdm(image_files):
        image_path = os.path.join(folder_path, file_name)
        score, metrics = analyze_dark_potential(image_path)
        
        if score >= threshold:
            candidates.append({
                'file_name': file_name,
                'path': image_path,
                'score': score,
                'metrics': metrics
            })
    
    # Sort candidates by score
    candidates.sort(key=lambda x: x['score'], reverse=True)
    return candidates

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    input_folder = os.path.join(parent_dir, "InstaAutomation", "KadhalThinamThinamInsta", "Other")
    
    if not os.path.exists(input_folder):
        print(f"Error: Input folder not found: {input_folder}")
        exit(1)
    
    candidates = find_potential_black_images(input_folder, threshold=70)
    
    print("\nPotential black image candidates:")
    print("=================================")
    for i, candidate in enumerate(candidates, 1):
        print(f"\n{i}. {candidate['file_name']}")
        print(f"   Score: {candidate['score']}/100")
        print(f"   Mean Brightness: {candidate['metrics']['mean_brightness']:.1f}")
        print(f"   Dark Pixel %: {candidate['metrics']['dark_pixel_percentage']:.1f}%")
        print(f"   Contrast (std): {candidate['metrics']['brightness_std']:.1f}")
        print(f"   Saturation: {candidate['metrics']['saturation_mean']:.1f}")

if __name__ == "__main__":
    main()
