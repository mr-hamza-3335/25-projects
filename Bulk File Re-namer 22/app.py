import streamlit as st
import os
import shutil

def rename_files(folder_path, prefix, suffix, numbering, replace_text, replace_with):
    if not os.path.exists(folder_path):
        return "Folder not found!"
    
    files = os.listdir(folder_path)
    files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
    
    if not files:
        return "No files found in the folder!"
    
    renamed_files = []
    for index, file in enumerate(files, start=1):
        file_name, file_ext = os.path.splitext(file)  # Get file name and extension
        
        # Replace text if applicable
        if replace_text and replace_with:
            file_name = file_name.replace(replace_text, replace_with)
        
        new_name = f"{prefix}{index if numbering else ''}{suffix}{file_ext}"
        
        old_path = os.path.join(folder_path, file)
        new_path = os.path.join(folder_path, new_name)
        shutil.move(old_path, new_path)
        renamed_files.append(new_name)
    
    return renamed_files

# Streamlit UI
st.title("📂 Bulk File Renamer")
st.write("Rename multiple files in a folder quickly!")

# Folder Selection with a file dialog
folder_path = st.text_input("Enter Folder Path Manually:", "")

prefix = st.text_input("Enter Prefix (Optional):", "File_")
suffix = st.text_input("Enter Suffix (Optional):", "")
numbering = st.checkbox("Add Numbering (e.g., File_1, File_2)")
replace_text = st.text_input("Text to Replace (Optional):", "")
replace_with = st.text_input("Replace With (Optional):", "")

# Folder Path Input Check
if folder_path:
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        st.success(f"Folder selected: {folder_path}")
    else:
        st.warning("Invalid Folder Path! Please make sure the folder exists.")
else:
    st.warning("Please enter a folder path.")

# Preview the renamed files
if st.button("Preview Files"):
    if folder_path and os.path.exists(folder_path):
        files = os.listdir(folder_path)
        files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
        
        if files:
            preview_files = []
            for i, f in enumerate(files):
                file_name, file_ext = os.path.splitext(f)
                if replace_text and replace_with:
                    file_name = file_name.replace(replace_text, replace_with)
                new_name = f"{prefix}{i+1 if numbering else ''}{suffix}{file_ext}"
                preview_files.append(new_name)
            
            st.write("### Preview of Renamed Files:")
            st.write(preview_files)
        else:
            st.warning("No files found in the folder!")
    else:
        st.error("Folder not selected or found!")

# Rename files when button is pressed
if st.button("Rename Files"):
    if folder_path:
        result = rename_files(folder_path, prefix, suffix, numbering, replace_text, replace_with)
        if isinstance(result, list):
            st.success("Files renamed successfully!")
            st.write("### Renamed Files:")
            st.write(result)
            
            # Auto-reset after renaming (clear folder input)
            st.session_state.folder_path = ""
        else:
            st.error(result)
    else:
        st.error("Please provide a valid folder path!")
