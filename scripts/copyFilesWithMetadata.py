import os
import shutil
import platform

if platform.system() == 'Windows':
    import win32file
    import pywintypes

def copy_file_with_metadata(src, dst):
    """
    Copies a file from src to dst, preserving metadata including the created date.
    
    :param src: Source file path
    :param dst: Destination file path
    """
    shutil.copy2(src, dst)  # Copy file along with metadata
    
    # Preserve the created date on Windows
    if platform.system() == 'Windows':
        st = os.stat(src)
        handle = win32file.CreateFile(
            dst, win32file.GENERIC_WRITE, 0, None,
            win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None
        )
        creation_time = pywintypes.Time(st.st_ctime)
        access_time = pywintypes.Time(st.st_atime)
        modification_time = pywintypes.Time(st.st_mtime)
        win32file.SetFileTime(handle, creation_time, access_time, modification_time)
        handle.close()
    else:
        # On Unix-like systems, we can only preserve access and modification times
        st = os.stat(src)
        os.utime(dst, (st.st_atime, st.st_mtime))

def copy_files_with_metadata(src_folder, dst_folder):
    """
    Copies all files from src_folder to dst_folder, preserving metadata.
    
    :param src_folder: Source folder path
    :param dst_folder: Destination folder path
    """
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    
    for file_name in os.listdir(src_folder):
        src_file = os.path.join(src_folder, file_name)
        dst_file = os.path.join(dst_folder, file_name)
        
        if os.path.isfile(src_file):
            copy_file_with_metadata(src_file, dst_file)
            print(f"Copied {src_file} to {dst_file}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    # src_folder = os.path.join(parent_dir, "ImagesUntil2025Feb24", "Full")
    src_folder = os.path.join(parent_dir, "KadhalThinamThinam")
    dst_folder1 = os.path.join(parent_dir,"InstaAutomation", "KadhalThinamThinamInsta")
    # dst_folder3 = os.path.join(parent_dir, "KarpanaiyoKadhalVasam")
    # dst_folder4 = os.path.join(parent_dir, "IdharaKavigal")

    
    print(f"Source folder: {src_folder}")
    print(f"Destination folder 1: {dst_folder1}")
    # print(f"Destination folder 2: {dst_folder2}")
    
    if not os.path.exists(src_folder):
        print(f"Error: Source folder not found: {src_folder}")
        exit(1)
    
    # copy_files_with_metadata(src_folder, dst_folder1)
    # copy_files_with_metadata(src_folder, dst_folder4)
    print("File copying complete!")

if __name__ == "__main__":
    main()
