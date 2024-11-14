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
        return [note.to_dict() for note in self.notes]

    @classmethod
    def from_list(cls, notes_list):
        project = cls()
        for note_data in notes_list:
            note = Note.from_dict(note_data)
            project.add_note(note)
        return project