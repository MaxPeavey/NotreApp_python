import json
import os
from class_files.ProjectClass import Project


class ProjectManager:
    def __init__(self, project, folder_path):
        self.project = project
        self.folder_path = folder_path
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        self.file_path = os.path.join(folder_path, "project.json")

    def save_project(self):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.project.to_list(), file, ensure_ascii=False, indent=4)

    # В функции load_project проверка на наличие файла
    def load_project(self):
        if os.path.exists(self.file_path):  # Проверка, существует ли файл project.json
            print(f"Путь к файлу {self.file_path} существует")
            with open(self.file_path, 'r', encoding='utf-8') as file:
                notes_list = json.load(file)
                self.project = Project.from_list(notes_list)
        else:        
            print(f"Путь к файлу {self.file_path} НЕ существует")
                