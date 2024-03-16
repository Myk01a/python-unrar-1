import tkinter as tk
from tkinter import messagebox
import patoolib
import string
import itertools
import time
from concurrent.futures import ThreadPoolExecutor
from tkinter import filedialog


def select_archive():
    archive_path = filedialog.askopenfilename(filetypes=[("Archive files", "*.rar *.zip")])
    entry_archive.delete(0, tk.END)
    entry_archive.insert(0, archive_path)


def select_dictionary():
    dictionary_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    entry_dictionary.delete(0, tk.END)
    entry_dictionary.insert(0, dictionary_path)


def read_dictionary(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        dictionary = [line.strip() for line in file]
    return dictionary


def try_password(archive_path, pwd):
    pwd_str = ''.join(pwd)
    try:
        patoolib.extract_archive(archive_path, password=pwd_str)
        return pwd_str
    except Exception as e:
        print("Помилка під час розпакування з паролем", pwd_str, ":", e)
        return None


def brut(password_combinations, batch_size=1000, archive_path=""):
    found_password = None
    start_time = time.time()
    passwords_tried = 0
    with ThreadPoolExecutor() as executor:
        batch = []
        for pwd in password_combinations:
            batch.append(pwd)
            passwords_tried += 1
            if len(batch) >= int(batch_size):
                futures = [executor.submit(try_password, archive_path, pwd) for pwd in batch]
                for future in futures:
                    result = future.result()
                    if result:
                        found_password = result
                        break
                if found_password:
                    break
                batch = []

            current_time = time.time()
            elapsed_time = current_time - start_time
            speed = passwords_tried / elapsed_time if elapsed_time > 0 else 0
            status_bar.config(text=f"Час: {elapsed_time:.2f} сек | Паролів перебрано: {passwords_tried} | Швидкість: {speed:.2f} паролів/сек")
            root.update()  # Оновити GUI

        if batch:
            futures = [executor.submit(try_password, archive_path, pwd) for pwd in batch]
            for future in futures:
                result = future.result()
                if result:
                    found_password = result
                    break

        end_time = time.time()
        elapsed_time = end_time - start_time
        speed = passwords_tried / elapsed_time if elapsed_time > 0 else 0
        status_bar.config(text=f"Час: {elapsed_time:.2f} сек | Паролів перебрано: {passwords_tried} | Швидкість: {speed:.2f} паролів/сек")
        root.update()  # Оновити GUI
        if found_password:
            messagebox.showinfo("Пароль знайдено", f"Знайдений пароль: {found_password}")
        else:
            messagebox.showinfo("Пароль не знайдено", "Пароль не був знайдений.")


def on_submit():
    choice = var.get()
    archive_path = entry_archive.get()
    dictionary_path = entry_dictionary.get()

    if choice == 1 and not dictionary_path:
        messagebox.showerror("Помилка", "Будь ласка, виберіть словник")
        return

    if choice == 1:
        dictionary = read_dictionary(dictionary_path)
        password_combinations = dictionary
    elif choice == 2:
        length_str = entry_length.get()
        if not length_str:
            messagebox.showerror("Помилка", "Будь ласка, введіть довжину пароля")
            return

        try:
            length = int(length_str)
        except ValueError:
            messagebox.showerror("Помилка", "Неправильне значення для довжини пароля")
            return

        password_options = ""
        if lowercase_var.get():
            password_options += string.ascii_lowercase
        if uppercase_var.get():
            password_options += string.ascii_uppercase
        if digits_var.get():
            password_options += string.digits
        if special_var.get():
            password_options += string.punctuation

        password_combinations = itertools.product(password_options, repeat=length)

    brut(password_combinations, archive_path=archive_path)


# Створення головного вікна
root = tk.Tk()
root.title("Підбір пароля")


frame_method = tk.Frame(root)
frame_method.pack(padx=10, pady=10)

var = tk.IntVar()
var.set(2)

tk.Radiobutton(frame_method, text="За зовнішнім словником", variable=var, value=1).pack(anchor="w")
tk.Radiobutton(frame_method, text="Лише символи", variable=var, value=2).pack(anchor="w")

label_length = tk.Label(root, text="Введіть довжину пароля:")
label_length.pack(pady=(10,0))
entry_length = tk.Entry(root)
entry_length.pack()

lowercase_var = tk.BooleanVar()
uppercase_var = tk.BooleanVar()
digits_var = tk.BooleanVar()
special_var = tk.BooleanVar()

lowercase_checkbox = tk.Checkbutton(root, text="Малі літери", variable=lowercase_var)
uppercase_checkbox = tk.Checkbutton(root, text="Великі літери", variable=uppercase_var)
digits_checkbox = tk.Checkbutton(root, text="Цифри", variable=digits_var)
special_checkbox = tk.Checkbutton(root, text="Спеціальні символи", variable=special_var)

lowercase_checkbox.pack(anchor="w")
uppercase_checkbox.pack(anchor="w")
digits_checkbox.pack(anchor="w")
special_checkbox.pack(anchor="w")

label_archive = tk.Label(root, text="Шлях до архіву:")
label_archive.pack(pady=(10,0))
entry_archive = tk.Entry(root)
entry_archive.pack()
button_select_archive = tk.Button(root, text="Вибрати архів", command=select_archive)
button_select_archive.pack(pady=(10,0))

label_dictionary = tk.Label(root, text="Шлях до словника:")
label_dictionary.pack(pady=(10,0))
entry_dictionary = tk.Entry(root)
entry_dictionary.pack()
button_select_dictionary = tk.Button(root, text="Вибрати словник", command=select_dictionary)
button_select_dictionary.pack(pady=(10,0))

button_submit = tk.Button(root, text="Почати пошук", command=on_submit)
button_submit.pack(pady=(10,0))

status_bar = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
