from datetime import datetime

class Note:
    def __init__(self, title="Без названия", category="личное", content="", creation_time=None, modification_time=None):
        self.title = title[:50] if title else "Без названия"
        self.category = category
        self.content = content
        self.creation_time = creation_time or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.modification_time = modification_time or self.creation_time

    def update(self, title=None, category=None, content=None):
        if title:
            self.title = title[:50]
        if category:
            self.category = category
        if content:
            self.content = content
        self.modification_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "title": self.title,
            "category": self.category,
            "content": self.content,
            "creation_time": self.creation_time,
            "modification_time": self.modification_time
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["category"], data["content"], data["creation_time"], data["modification_time"])