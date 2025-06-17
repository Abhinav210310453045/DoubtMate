import os
import shutil

source_dir = 'jesc101_text_pdfminer'
dest_dir = 'New folder'

# Ensure destination directory exists
os.makedirs(dest_dir, exist_ok=True)

for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.endswith('.txt'):
            src_path = os.path.join(root, file)
            dest_path = os.path.join(dest_dir, file)
            # Overwrite if file exists
            shutil.copy2(src_path, dest_path)

print('All .txt files have been copied to', dest_dir)
