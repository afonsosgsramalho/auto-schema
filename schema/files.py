import os
import logging

def create_files_folder(file_path):
    if not os.path.exists(file_path):
            try:
                os.makedirs(file_path)
            except Exception as e:
                print(e)
                raise