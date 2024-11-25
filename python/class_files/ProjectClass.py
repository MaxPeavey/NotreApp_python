import json
from datetime import datetime
from class_files.NotesClass import Note

class Project:
    def __init__(self):
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def remove_note_by_title(self, title):
        self.notes = [note for note in self.notes if note.title != title]

    def get_note_by_title(self, title):
        for note in self.notes:
            if note.title == title:
                return note
        return None

    def to_list(self):
        # Преобразует список объектов Note в список словарей, пригодных для JSON
        return [note.to_dict() for note in self.notes]

    @staticmethod
    def from_json(json_data):
        project = Project()
        for item in json_data:
            note = Note(
                title=item['title'],
                category=item['category'],
                content=item['content'],
                creation_time=datetime.strptime(item['creation_time'], '%Y-%m-%d %H:%M:%S'),
                modification_time=datetime.strptime(item['modification_time'], '%Y-%m-%d %H:%M:%S')
            )
            project.add_note(note)
        return project
