import os
import shutil

def move_images_to_single_folder(source_folder, destination_folder):
    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)
    
    # Iterate through all subfolders in the source folder
    for subfolder_name in os.listdir(source_folder):
        subfolder_path = os.path.join(source_folder, subfolder_name)
        
        if os.path.isdir(subfolder_path):
            # Iterate through all files in the subfolder
            for file_name in os.listdir(subfolder_path):
                if file_name.lower().endswith(('png', 'jpg', 'jpeg')):
                    source_file_path = os.path.join(subfolder_path, file_name)
                    destination_file_path = os.path.join(destination_folder, file_name)
                    
                    # Move the file to the destination folder
                    shutil.move(source_file_path, destination_file_path)
                    print(f"Moved {file_name} to {destination_folder}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    source_folder = os.path.join(parent_dir, "ImagesUntil2025Feb24", "New Folder")
    destination_folder = os.path.join(parent_dir, "ImagesUntil2025Feb24", "AllImages")
    
    move_images_to_single_folder(source_folder, destination_folder)
    print("All images have been moved to the single folder.")