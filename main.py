import patoolib
import string
import itertools
import time


def read_dictionary(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        dictionary = [line.strip() for line in file]
    return dictionary


def brut(password_combinations):
    start_time = time.time()
    for pwd in password_combinations:
        try:
            pwd_str = ''.join(pwd)
            patoolib.extract_archive("text2.rar", password=pwd_str)
            print("Успішно розпаковано з паролем:", pwd_str)
            break
        except Exception as e:
            print("Помилка під час розпакування з паролем", pwd_str, ":", e)
    else:
        print("Архів не був розпакований. Не вдалося знайти правильний пароль.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Час, затрачений на пошук пароля: {:.2f} секунд".format(elapsed_time))


def menu():
    print("Оберіть спосіб перебору та кількість символів у паролі:")
    print("1. За зовнішнім словником")
    print("2. Лише цифри")
    print("3. Малі  літери англійського алфавіту")
    choice = input("Ваш вибір: ")

    if choice == '1':
        dictionary = read_dictionary('dictionary.txt')
        password_combinations = dictionary
    elif choice == '2':
        password_options = string.digits
        password_length = int(input("Введіть кількість символів у паролі: "))
        password_combinations = itertools.product(password_options, repeat=password_length)
    elif choice == '3':
        password_options = string.ascii_lowercase
        password_length = int(input("Введіть кількість символів у паролі: "))
        password_combinations = itertools.product(password_options, repeat=password_length)
    else:
        print("Невірний вибір.")
        return

    brut(password_combinations)


menu()
