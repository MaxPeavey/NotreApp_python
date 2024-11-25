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
        # Открываем файл для чтения существующих данных
        existing_notes = []
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                try:
                    existing_notes = json.load(file)
                except json.JSONDecodeError:
                    print("Ошибка при чтении JSON-файла. Возможно, файл поврежден.")
        
        # Сохраняем только уникальные заметки, чтобы не дублировать
        new_notes = self.project.to_list()
        combined_notes = self._merge_notes(existing_notes, new_notes)

        # Перезаписываем файл с обновленными данными
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(combined_notes, file, ensure_ascii=False, indent=4)

    def _merge_notes(self, existing_notes, new_notes):
        # Метод для слияния существующих и новых заметок без дублирования
        existing_titles = {note['title'] for note in existing_notes}
        merged_notes = existing_notes + [note for note in new_notes if note['title'] not in existing_titles]
        return merged_notes
