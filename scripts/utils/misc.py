import os 
import shutil 

def clear_folder(folder_path):
    try:
        # Iterate over all files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # Check if the current path is a file
            if os.path.isfile(file_path):
                # Remove the file
                os.remove(file_path)
                print(f"Removed: {file_path}")
        print(f"All files in '{folder_path}' have been cleared.")
    except Exception as e:
        print(f"Error clearing files in '{folder_path}': {e}")

def copy_files(source_folder, target_folder):
    for item in os.listdir(source_folder):
        source_path = os.path.join(source_folder, item)
        target_path = os.path.join(target_folder, item)
        try:
            if os.path.isdir(source_path):
                shutil.copytree(source_path, target_path)
            else:
                shutil.copy2(source_path, target_path)
        except Exception as e:
            print(f'Failed to copy {source_path} to {target_path}. Reason: {e}')