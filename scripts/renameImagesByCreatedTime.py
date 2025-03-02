import os
import platform
from datetime import datetime

if platform.system() == 'Windows':
    import win32file
    import pywintypes

def get_created_date(file_path):
    """
    Gets the created date of a file.
    
    :param file_path: Path to the file
    :return: Created date of the file
    """
    if platform.system() == 'Windows':
        handle = win32file.CreateFile(
            file_path, win32file.GENERIC_READ, win32file.FILE_SHARE_READ, None,
            win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None
        )
        created_date = win32file.GetFileTime(handle)[0]
        handle.close()
        return created_date
    else:
        st = os.stat(file_path)
        return datetime.fromtimestamp(st.st_ctime)

def rename_images_by_created_time(folder_path):
    """
    Renames images in the specified folder based on their created time.
    
    :param folder_path: Path to the folder
    """
    images = []
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith(('png', 'jpg', 'jpeg')):
            created_date = get_created_date(file_path)
            images.append((created_date, file_name))
    
    # Sort images by created date
    images.sort()
    
    # Skip the specified numbers
    skip_numbers = {286, 328, 343, 352}
    counter = 1
    
    for created_date, file_name in images:
        while counter in skip_numbers:
            counter += 1
        
        new_file_name = f"KadhalThinamThinam{counter}.png"
        old_file_path = os.path.join(folder_path, file_name)
        new_file_path = os.path.join(folder_path, new_file_name)
        
        os.rename(old_file_path, new_file_path)
        print(f"Renamed {file_name} to {new_file_name}")
        
        counter += 1

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    folder_path = os.path.join(parent_dir, "KadhalThinamThinam")
    
    print(f"Folder path: {folder_path}")
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder not found: {folder_path}")
        exit(1)
    
    rename_images_by_created_time(folder_path)
    print("Image renaming complete!")

if __name__ == "__main__":
    main()
