from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import os

history_file = 'history.csv'
last_result = None


def prepare_file():
    if not os.path.exists(history_file):
        with open(history_file, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Дата', 'Длина текста', 'Символы', 'Слова', 'Строки', 'Пробелы'])


def analyze_text():
    global last_result
    text = text_box.get('1.0', 'end-1c')

    if text == '':
        chars = 0
        words = 0
        lines = 0
        spaces = 0
    else:
        chars = len(text)
        words = len(text.split())
        lines = text.count('\n') + 1
        spaces = text.count(' ')

    result_chars_value.config(text=str(chars))
    result_words_value.config(text=str(words))
    result_lines_value.config(text=str(lines))
    result_spaces_value.config(text=str(spaces))

    last_result = {
        'date': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
        'length': len(text),
        'chars': chars,
        'words': words,
        'lines': lines,
        'spaces': spaces
    }



def save_result():
    global last_result

    if last_result is None:
        messagebox.showwarning('Внимание', 'Сначала выполните анализ текста.')
        return

    with open(history_file, 'a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([
            last_result['date'],
            last_result['length'],
            last_result['chars'],
            last_result['words'],
            last_result['lines'],
            last_result['spaces']
        ])

    messagebox.showinfo('Сохранение', 'Результаты сохранены в файл history.csv')



def clear_all():
    global last_result
    text_box.delete('1.0', END)
    result_chars_value.config(text='0')
    result_words_value.config(text='0')
    result_lines_value.config(text='0')
    result_spaces_value.config(text='0')
    last_result = None


prepare_file()

window = Tk()
window.title('Анализатор текста')
window.geometry('760x660')
window.resizable(False, False)

main_frame = Frame(window, padx=15, pady=15)
main_frame.pack(fill=BOTH, expand=True)

title_label = Label(main_frame, text='Анализатор текста', font=('Arial', 18, 'bold'))
title_label.pack(pady=(0, 10))

instruction_label = Label(main_frame, text='Введите текст и нажмите кнопку «Анализировать»', font=('Arial', 11))
instruction_label.pack(pady=(0, 10))

text_box = Text(main_frame, width=85, height=14, font=('Arial', 11), wrap=WORD)
text_box.pack()

buttons_frame = Frame(main_frame)
buttons_frame.pack(pady=12)

analyze_button = Button(buttons_frame, text='Анализировать', width=18, command=analyze_text)
analyze_button.grid(row=0, column=0, padx=5)

save_button = Button(buttons_frame, text='Сохранить результат', width=18, command=save_result)
save_button.grid(row=0, column=1, padx=5)

clear_button = Button(buttons_frame, text='Очистить', width=18, command=clear_all)
clear_button.grid(row=0, column=2, padx=5)

exit_button = Button(buttons_frame, text='Выход', width=18, command=window.destroy)
exit_button.grid(row=0, column=3, padx=5)

result_frame = LabelFrame(main_frame, text='Результаты анализа', padx=15, pady=15, font=('Arial', 11, 'bold'))
result_frame.pack(fill=X, pady=10)

result_chars_label = Label(result_frame, text='Количество символов:', font=('Arial', 11))
result_chars_label.grid(row=0, column=0, sticky='w', pady=4)
result_chars_value = Label(result_frame, text='0', font=('Arial', 11, 'bold'))
result_chars_value.grid(row=0, column=1, sticky='w', padx=10)

result_words_label = Label(result_frame, text='Количество слов:', font=('Arial', 11))
result_words_label.grid(row=1, column=0, sticky='w', pady=4)
result_words_value = Label(result_frame, text='0', font=('Arial', 11, 'bold'))
result_words_value.grid(row=1, column=1, sticky='w', padx=10)

result_lines_label = Label(result_frame, text='Количество строк:', font=('Arial', 11))
result_lines_label.grid(row=2, column=0, sticky='w', pady=4)
result_lines_value = Label(result_frame, text='0', font=('Arial', 11, 'bold'))
result_lines_value.grid(row=2, column=1, sticky='w', padx=10)

result_spaces_label = Label(result_frame, text='Количество пробелов:', font=('Arial', 11))
result_spaces_label.grid(row=3, column=0, sticky='w', pady=4)
result_spaces_value = Label(result_frame, text='0', font=('Arial', 11, 'bold'))
result_spaces_value.grid(row=3, column=1, sticky='w', padx=10)

file_label = Label(main_frame, text='После сохранения результаты записываются в файл history.csv', font=('Arial', 10))
file_label.pack(pady=(5, 0))

window.mainloop()
