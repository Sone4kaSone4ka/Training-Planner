import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("План тренировок")
        self.root.geometry("800x600")
        
        # Основные виджеты
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        # Форма ввода
        tk.Label(root, text="Дата (ДД.ММ.ГГГГ):").pack()
        self.date_entry = tk.Entry(root)
        self.date_entry.pack()
        
        tk.Label(root, text="Тип тренировки:").pack()
        self.type_entry = tk.Entry(root)
        self.type_entry.pack()
        
        tk.Label(root, text="Длительность (мин):").pack()
        self.duration_entry = tk.Entry(root)
        self.duration_entry.pack()
        
        # Кнопка добавления
        tk.Button(root, text="Добавить тренировку", command=self.add_training).pack()
        
        # Список тренировок
        self.listbox = tk.Listbox(root, width=80, height=20)
        self.listbox.pack()
        
        # Фильтры
        tk.Label(root, text="Фильтр по типу:").pack()
        self.filter_type = tk.Entry(root)
        self.filter_type.pack()
        
        tk.Button(root, text="Применить фильтр", command=self.apply_filter).pack()
        
    def add_training(self):
        try:
            date = self.date_entry.get()
            training_type = self.type_entry.get()
            duration = int(self.duration_entry.get())
            
            if not self.validate_date(date) or duration <= 0:
                messagebox.showerror("Ошибка", "Неверные данные")
                return
            
            self.trainings.append({
                "date": date,
                "type": training_type,
                "duration": duration
            })
            self.save_data()
            self.update_list()
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть числом")
    
    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
            return True
        except ValueError:
            return False
    
    def update_list(self):
        self.listbox.delete(0, tk.END)
        for training in self.trainings:
            self.listbox.insert(tk.END, f"{training['date']} - {training['type']} ({training['duration']} мин)")
    
    def apply_filter(self):
        filter_text = self.filter_type.get()
        filtered = [t for t in self.trainings if filter_text.lower() in t['type'].lower()]
        self.listbox.delete(0, tk.END)
        for training in filtered:
            self.listbox.insert(tk.END, f"{training['date']} - {training['type']} ({training['duration']} мин)")
    
    def load_data(self):
        try:
            with open('trainings.json', 'r') as file:
                self.trainings = json.load(file)
        except FileNotFoundError:
            self.trainings = []
    
    def save_data(self):
        with open('trainings.json', 'w') as file:
            json.dump(self.trainings, file, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()