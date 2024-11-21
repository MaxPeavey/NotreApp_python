import os
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from tkinter import ttk
from datetime import datetime
import json
from class_files.NotesClass import Note
from class_files.ProjectClass import Project
from class_files.ProjectMngClass import ProjectManager
from class_files.About import About

class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notes Manager")

        # Создаем папку на Рабочем столе для хранения заметок
        self.notes_folder = os.path.join(os.path.expanduser("~"), "Desktop", "Notes")
        self.project = Project()
        self.manager = ProjectManager(self.project, self.notes_folder)

        # Проверка на наличие project.json и загрузка данных, если файл существует
        if os.path.exists(self.manager.file_path):
            print(f"{self.manager.file_path} путь к файлу\n")
            self.manager.load_project()

        # Интерфейс
        self.create_ui()

    def create_ui(self):
        #Верхний фрейм
        top_frame=tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X,)

        about_button=tk.Button(top_frame, text="About", command=self.About_window)
        about_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Левый фрейм для списка файлов
        left_frame = tk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y,after=top_frame)

        self.notes_listbox = tk.Listbox(left_frame, width=40)
        self.notes_listbox.pack(fill=tk.Y, padx=5, pady=5,expand=True)
        self.notes_listbox.bind('<<ListboxSelect>>', self.display_note_content)

        # Правый фрейм для отображения содержимого заметки
        right_frame = tk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.content_text = tk.Text(right_frame, wrap=tk.WORD)
        self.content_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Нижняя панель с кнопками
        bottom_frame = tk.Frame(left_frame)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        add_button = tk.Button(bottom_frame, text="+", command=self.create_note)
        add_button.pack(side=tk.RIGHT, padx=5, pady=5)

        delete_button = tk.Button(bottom_frame, text="-", command=self.delete_note)
        delete_button.pack(side=tk.RIGHT, padx=5, pady=5)

        edit_button = tk.Button(top_frame, text="✎", command=self.edit_note)
        edit_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Загрузить список заметок
        self.load_notes_list()

        #О программе (Окно)
    def About_window(self):
        About_window= tk.Toplevel(self.root)
        About_window.geometry("250x120")
        About_window.resizable(False,False)
        About_window.title("O приложение")
        tk.Label(About_window, text="NoteApp",font=("Impact", 20, "bold"),justify="center" ).pack()
        tk.Label(About_window, text=f"Автор: {info.author}\n v{info.version}\n {info.email}\n {info.gihub}",justify="left").pack(side=tk.LEFT,padx=5)

    def load_notes_list(self):
        self.notes_listbox.delete(0, tk.END)
        for note in self.project.notes:
            self.notes_listbox.insert(tk.END, note.title)

    def display_note_content(self, event):
        selected_index = self.notes_listbox.curselection()
        if selected_index:
            selected_title = self.notes_listbox.get(selected_index)
            note = self.project.get_note_by_title(selected_title)
            if note:
                self.content_text.delete(1.0, tk.END)
                self.content_text.insert(tk.END, f"Категория: {note.category}\n")
                self.content_text.insert(tk.END, f"Создано: {note.creation_time}\n")
                self.content_text.insert(tk.END, f"Изменено: {note.modification_time}\n\n")
                self.content_text.insert(tk.END, note.content)

    def create_note_window(self, note=None):
        def save_note():
            title = title_entry.get()[:50] or "Без названия"
            category = category_combobox.get()
            content = content_text.get(1.0, tk.END).strip()
            
            if note:
                note.update(title=title, category=category, content=content)
            else:
                new_note = Note(title=title, category=category, content=content)
                self.project.add_note(new_note)
            
            self.manager.save_project()
            self.load_notes_list()
            note_window.destroy()

        note_window = tk.Toplevel(self.root)
        note_window.title("Создание/Редактирование заметки")

        # Поле для названия
        tk.Label(note_window, text="Название:").pack()
        title_entry = tk.Entry(note_window, width=50)
        title_entry.pack(pady=5)
        if note:
            title_entry.insert(0, note.title)

        # Поле для даты создания
        creation_time_label = tk.Label(note_window, text=f"Дата создания: {note.creation_time if note else datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        creation_time_label.pack(pady=5)

        # Поле для даты модификации (если редактируется)
        if note:
            modification_time_label = tk.Label(note_window, text=f"Дата модификации: {note.modification_time}")
            modification_time_label.pack(pady=5)

        # Поле для выбора категории
        tk.Label(note_window, text="Категория:").pack()
        category_combobox = ttk.Combobox(note_window, values=["работа", "учеба", "личное"], state="readonly")
        category_combobox.pack(pady=5)
        category_combobox.set(note.category if note else "личное")

        # Поле для текста заметки
        tk.Label(note_window, text="Текст заметки:").pack()
        content_text = tk.Text(note_window, wrap=tk.WORD, height=15)
        content_text.pack(fill=tk.BOTH, padx=5, pady=5)
        if note:
            content_text.insert(tk.END, note.content)

        # Кнопка Сохранить
        save_button = tk.Button(note_window, text="Сохранить", command=save_note)
        save_button.pack(pady=5)

    def create_note(self):
        self.create_note_window()

    def edit_note(self):
        selected_index = self.notes_listbox.curselection()
        if selected_index:
            selected_title = self.notes_listbox.get(selected_index)
            note = self.project.get_note_by_title(selected_title)
            if note:
                self.create_note_window(note)

    def delete_note(self):
        selected_index = self.notes_listbox.curselection()
        if selected_index:
            selected_title = self.notes_listbox.get(selected_index)
            if messagebox.askyesno("Удалить заметку", f"Вы уверены, что хотите удалить заметку '{selected_title}'?"):
                self.project.remove_note_by_title(selected_title)
                self.manager.save_project()
                self.load_notes_list()

# Запуск приложения
if __name__ == "__main__":
    info=About("Max Peavey","0.8.0 Beta","123@mail.ru","12345/git")
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()
