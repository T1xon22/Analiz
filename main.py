import csv
import os
import re
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox


class TextAnalyzerApp:
    HISTORY_FILE = 'history.csv'
    CSV_HEADERS = [
        'Дата',
        'Символы всего',
        'Символы без пробелов',
        'Слова',
        'Уникальные слова',
        'Строки',
        'Пробелы',
        'Средняя длина слова'
    ]

    def __init__(self, root):
        self.root = root
        self.root.title('Анализатор текста')
        self.root.geometry('820x620')
        self.root.resizable(False, False)

        self.last_result = None
        self.result_window = None
        self.history_window = None
        self.result_value_labels = {}
        self.history_tree = None

        self.live_counter_var = tk.StringVar(value='Текущая длина текста: 0 символов')
        self.history_count_var = tk.StringVar(value='Записей в истории: 0')

        self.prepare_file()
        self.create_main_window()

    def prepare_file(self):
        if not os.path.exists(self.HISTORY_FILE):
            with open(self.HISTORY_FILE, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(self.CSV_HEADERS)

    def create_main_window(self):
        main_frame = tk.Frame(self.root, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            main_frame,
            text='Анализатор текста',
            font=('Arial', 18, 'bold')
        )
        title_label.pack(pady=(0, 10))

        instruction_label = tk.Label(
            main_frame,
            text='Введите текст, нажмите «Анализировать», затем откройте окна результатов и истории',
            font=('Arial', 11)
        )
        instruction_label.pack(pady=(0, 10))

        self.text_box = tk.Text(
            main_frame,
            width=90,
            height=16,
            font=('Arial', 11),
            wrap=tk.WORD
        )
        self.text_box.pack()
        self.text_box.bind('<KeyRelease>', self.update_live_counter)

        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(pady=12)

        tk.Button(
            buttons_frame,
            text='Анализировать',
            width=18,
            command=self.analyze_text
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(
            buttons_frame,
            text='Окно результатов',
            width=18,
            command=self.open_result_window
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            buttons_frame,
            text='Окно истории',
            width=18,
            command=self.open_history_window
        ).grid(row=0, column=2, padx=5, pady=5)

        tk.Button(
            buttons_frame,
            text='Сохранить результат',
            width=18,
            command=self.save_result
        ).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(
            buttons_frame,
            text='Очистить',
            width=18,
            command=self.clear_all
        ).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            buttons_frame,
            text='Выход',
            width=18,
            command=self.root.destroy
        ).grid(row=1, column=2, padx=5, pady=5)

        live_counter_label = tk.Label(
            main_frame,
            textvariable=self.live_counter_var,
            font=('Arial', 10, 'italic')
        )
        live_counter_label.pack(pady=(5, 5))

        file_label = tk.Label(
            main_frame,
            text='История анализов сохраняется в файл history.csv',
            font=('Arial', 10)
        )
        file_label.pack(pady=(5, 0))

    def get_words(self, text):
        return re.findall(r"[A-Za-zА-Яа-яЁё0-9]+(?:[-'][A-Za-zА-Яа-яЁё0-9]+)?", text.lower())

    def update_live_counter(self, event=None):
        text = self.text_box.get('1.0', 'end-1c')
        self.live_counter_var.set(f'Текущая длина текста: {len(text)} символов')

    def analyze_text(self, event=None):
        text = self.text_box.get('1.0', 'end-1c')

        if not text:
            chars_total = 0
            chars_without_spaces = 0
            words_count = 0
            unique_words = 0
            lines_count = 0
            spaces_count = 0
            avg_word_length = 0
        else:
            chars_total = len(text)
            chars_without_spaces = len(text.replace(' ', '').replace('\n', '').replace('\t', ''))
            words = self.get_words(text)
            words_count = len(words)
            unique_words = len(set(words))
            lines_count = text.count('\n') + 1
            spaces_count = text.count(' ')
            avg_word_length = round(sum(len(word) for word in words) / words_count, 2) if words_count else 0

        self.last_result = {
            'date': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
            'chars_total': chars_total,
            'chars_without_spaces': chars_without_spaces,
            'words': words_count,
            'unique_words': unique_words,
            'lines': lines_count,
            'spaces': spaces_count,
            'avg_word_length': avg_word_length
        }

        self.update_result_window()

        if self.result_window is not None and self.result_window.winfo_exists():
            self.result_window.lift()

    def save_result(self):
        if self.last_result is None:
            messagebox.showwarning('Внимание', 'Сначала выполните анализ текста.')
            return

        with open(self.HISTORY_FILE, 'a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([
                self.last_result['date'],
                self.last_result['chars_total'],
                self.last_result['chars_without_spaces'],
                self.last_result['words'],
                self.last_result['unique_words'],
                self.last_result['lines'],
                self.last_result['spaces'],
                self.last_result['avg_word_length']
            ])

        messagebox.showinfo('Сохранение', 'Результаты сохранены в файл history.csv')
        self.load_history()

    def copy_result(self):
        if self.last_result is None:
            messagebox.showwarning('Внимание', 'Нет результатов для копирования.')
            return

        result_text = (
            f"Дата анализа: {self.last_result['date']}\n"
            f"Символы всего: {self.last_result['chars_total']}\n"
            f"Символы без пробелов: {self.last_result['chars_without_spaces']}\n"
            f"Слова: {self.last_result['words']}\n"
            f"Уникальные слова: {self.last_result['unique_words']}\n"
            f"Строки: {self.last_result['lines']}\n"
            f"Пробелы: {self.last_result['spaces']}\n"
            f"Средняя длина слова: {self.last_result['avg_word_length']}"
        )

        self.root.clipboard_clear()
        self.root.clipboard_append(result_text)
        self.root.update()
        messagebox.showinfo('Копирование', 'Результаты скопированы в буфер обмена.')

    def clear_all(self):
        self.text_box.delete('1.0', tk.END)
        self.last_result = None
        self.update_live_counter()
        self.update_result_window()

    def open_result_window(self):
        if self.result_window is not None and self.result_window.winfo_exists():
            self.result_window.lift()
            self.result_window.focus_force()
            return

        self.result_window = tk.Toplevel(self.root)
        self.result_window.title('Результаты анализа')
        self.result_window.geometry('430x360')
        self.result_window.resizable(False, False)
        self.result_window.protocol('WM_DELETE_WINDOW', self.close_result_window)

        frame = tk.Frame(self.result_window, padx=15, pady=15)
        frame.pack(fill=tk.BOTH, expand=True)

        title = tk.Label(frame, text='Результаты анализа', font=('Arial', 16, 'bold'))
        title.pack(pady=(0, 12))

        info_frame = tk.LabelFrame(
            frame,
            text='Статистика',
            padx=15,
            pady=10,
            font=('Arial', 11, 'bold')
        )
        info_frame.pack(fill=tk.BOTH, expand=True)

        fields = [
            ('Символы всего:', 'chars_total'),
            ('Символы без пробелов:', 'chars_without_spaces'),
            ('Количество слов:', 'words'),
            ('Уникальные слова:', 'unique_words'),
            ('Количество строк:', 'lines'),
            ('Количество пробелов:', 'spaces'),
            ('Средняя длина слова:', 'avg_word_length'),
        ]

        self.result_value_labels = {}

        for index, (label_text, key) in enumerate(fields):
            label = tk.Label(info_frame, text=label_text, font=('Arial', 11))
            label.grid(row=index, column=0, sticky='w', pady=4)

            value_label = tk.Label(info_frame, text='0', font=('Arial', 11, 'bold'))
            value_label.grid(row=index, column=1, sticky='w', padx=10)
            self.result_value_labels[key] = value_label

        buttons_frame = tk.Frame(frame)
        buttons_frame.pack(pady=12)

        tk.Button(buttons_frame, text='Копировать', width=15, command=self.copy_result).grid(row=0, column=0, padx=5)
        tk.Button(buttons_frame, text='Сохранить', width=15, command=self.save_result).grid(row=0, column=1, padx=5)
        tk.Button(buttons_frame, text='Закрыть', width=15, command=self.close_result_window).grid(row=0, column=2, padx=5)

        self.update_result_window()

    def close_result_window(self):
        self.result_value_labels = {}
        if self.result_window is not None and self.result_window.winfo_exists():
            self.result_window.destroy()
        self.result_window = None

    def update_result_window(self):
        if not self.result_value_labels:
            return

        if self.last_result is None:
            empty_values = {
                'chars_total': '0',
                'chars_without_spaces': '0',
                'words': '0',
                'unique_words': '0',
                'lines': '0',
                'spaces': '0',
                'avg_word_length': '0',
            }
            for key, label in self.result_value_labels.items():
                if label.winfo_exists():
                    label.config(text=empty_values[key])
            return

        for key, label in self.result_value_labels.items():
            if label.winfo_exists():
                label.config(text=str(self.last_result[key]))

    def open_history_window(self):
        if self.history_window is not None and self.history_window.winfo_exists():
            self.load_history()
            self.history_window.lift()
            self.history_window.focus_force()
            return

        self.history_window = tk.Toplevel(self.root)
        self.history_window.title('История анализов')
        self.history_window.geometry('980x420')
        self.history_window.resizable(False, False)
        self.history_window.protocol('WM_DELETE_WINDOW', self.close_history_window)

        frame = tk.Frame(self.history_window, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        title = tk.Label(frame, text='История анализов', font=('Arial', 16, 'bold'))
        title.pack(pady=(0, 10))

        table_frame = tk.Frame(frame)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = (
            'date',
            'chars_total',
            'chars_without_spaces',
            'words',
            'unique_words',
            'lines',
            'spaces',
            'avg_word_length'
        )

        self.history_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=13)

        headings = {
            'date': 'Дата',
            'chars_total': 'Символы всего',
            'chars_without_spaces': 'Без пробелов',
            'words': 'Слова',
            'unique_words': 'Уникальные',
            'lines': 'Строки',
            'spaces': 'Пробелы',
            'avg_word_length': 'Ср. длина слова'
        }

        widths = {
            'date': 150,
            'chars_total': 110,
            'chars_without_spaces': 120,
            'words': 90,
            'unique_words': 100,
            'lines': 80,
            'spaces': 90,
            'avg_word_length': 120
        }

        for col in columns:
            self.history_tree.heading(col, text=headings[col])
            self.history_tree.column(col, width=widths[col], anchor='center')

        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar_y.set)

        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        info_label = tk.Label(frame, textvariable=self.history_count_var, font=('Arial', 10))
        info_label.pack(pady=(8, 5))

        buttons_frame = tk.Frame(frame)
        buttons_frame.pack()

        tk.Button(buttons_frame, text='Обновить', width=18, command=self.load_history).grid(row=0, column=0, padx=5)
        tk.Button(buttons_frame, text='Очистить историю', width=18, command=self.clear_history).grid(row=0, column=1, padx=5)
        tk.Button(buttons_frame, text='Закрыть', width=18, command=self.close_history_window).grid(row=0, column=2, padx=5)

        self.load_history()

    def close_history_window(self):
        if self.history_window is not None and self.history_window.winfo_exists():
            self.history_window.destroy()
        self.history_window = None
        self.history_tree = None

    def load_history(self):
        if self.history_tree is None or not self.history_tree.winfo_exists():
            return

        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        count = 0

        if os.path.exists(self.HISTORY_FILE):
            with open(self.HISTORY_FILE, 'r', newline='', encoding='utf-8-sig') as file:
                reader = csv.reader(file, delimiter=';')
                next(reader, None)

                for row in reader:
                    if row:
                        self.history_tree.insert('', tk.END, values=row)
                        count += 1

        self.history_count_var.set(f'Записей в истории: {count}')

    def clear_history(self):
        answer = messagebox.askyesno('Подтверждение', 'Вы действительно хотите очистить историю?')
        if not answer:
            return

        with open(self.HISTORY_FILE, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(self.CSV_HEADERS)

        self.load_history()
        messagebox.showinfo('История', 'История успешно очищена.')


def main():
    root = tk.Tk()
    app = TextAnalyzerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()