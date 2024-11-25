# class_files/NotesClass.py

from datetime import datetime

class Note:
    def __init__(self, title, category, content, creation_time=None, modification_time=None):
        self.title = title
        self.category = category
        self.content = content
        self.creation_time = creation_time or datetime.now()
        self.modification_time = modification_time or datetime.now()

    def to_dict(self):
        # Преобразуем объекты datetime в строку перед сохранением в JSON
        return {
            "title": self.title,
            "category": self.category,
            "content": self.content,
            "creation_time": self.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            "modification_time": self.modification_time.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def update_content(self, title=None, category=None, content=None):
        # Обновляет содержимое заметки
        if title:
            self.title = title
        if category:
            self.category = category
        if content:
            self.content = content
        # Обновляем время модификации каждый раз при изменении
        self.modification_time = datetime.now()
