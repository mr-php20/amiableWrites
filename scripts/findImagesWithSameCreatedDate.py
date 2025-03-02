import os
from collections import defaultdict
import platform
from datetime import datetime

if platform.system() == 'Windows':
    import win32file
    import pywintypes

def get_created_date(file_path):
    """
    Gets the created date of a file.
    
    :param file_path: Path to the file
    :return: Created date of the file (date part only)
    """
    if platform.system() == 'Windows':
        handle = win32file.CreateFile(
            file_path, win32file.GENERIC_READ, win32file.FILE_SHARE_READ, None,
            win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None
        )
        created_date = win32file.GetFileTime(handle)[0]
        handle.close()
        return created_date.date()
    else:
        st = os.stat(file_path)
        return datetime.fromtimestamp(st.st_ctime).date()

def find_images_with_same_created_date(folder_path):
    """
    Finds images with the same created date in the specified folder.
    
    :param folder_path: Path to the folder
    """
    created_date_dict = defaultdict(int)
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith(('png', 'jpg', 'jpeg')):
            created_date = get_created_date(file_path)
            created_date_dict[created_date] += 1
    
    for created_date, count in created_date_dict.items():
        if count > 1:
            print(f"Created date {created_date} has {count} images")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    folder_path = os.path.join(parent_dir, "KadhalThinamThinam")
    
    print(f"Folder path: {folder_path}")
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder not found: {folder_path}")
        exit(1)
    
    find_images_with_same_created_date(folder_path)
    print("Image search complete!")

if __name__ == "__main__":
    main()
