from tkinter import *
from LoadToExcel import LoadData
from tkinter import font
from tkinter import messagebox as mb
from functools import wraps


def event(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        make = func(*args, **kwargs)
        start()
        return make

    return wrapper


def start():
    root = Tk()
    root.title("Создание таблиц для авито")

    vals = {"Прямые столы": "straight tables",
            "Угловые столы": "corner tables",
            "Директорская мебель": "director office",
            "Компьютерные кресла": "comp armchair",
            "Стулья": "chairs",
            "Шкафы": "closet",
            "Тумбы": "cabinet"}

    key = list(vals.keys())
    variable = Variable(value=key)
    listbox = Listbox(listvariable=variable, width=30, relief="solid",
                      font=font.Font(family="Times New Roman", size=12))
    label = Label(text="Введите колличесто сообщений(фото), которое нужно обработать",
                  font=font.Font(family="Times New Roman", size=12))
    enter_count = Entry()

    but_pars = Button(text="Добавить товар", command=lambda: add_goods(vals[key[listbox.curselection()[0]]],
                                                                       enter_count.get(), root))
    but_download = Button(text="Скачать таблицу", command=lambda: download(vals[key[listbox.curselection()[0]]]))

    listbox.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)
    label.grid(row=1, column=0, columnspan=2, sticky="w", padx=3, pady=5)
    enter_count.grid(row=2, column=0, columnspan=2, sticky="w", padx=3, pady=5)
    but_pars.grid(row=3, column=0, sticky="w", padx=3, pady=5)
    but_download.grid(row=3, column=1, sticky="w", padx=3, pady=5)
    root.mainloop()


@event
def add_goods(channel, con, root):
    try:
        if not con.isdigit():
            mb.showerror('Error', "Введите количество сообщений для обработки")
        else:
            data = LoadData(channel)
            root.destroy()
            data.start_pars(int(con))
    except IndexError:
        mb.showerror("Error", "Выберите канал для скачивания данных!")


def download(channel):
    try:
        data = LoadData(channel)
        data.table_for_avito()
    except IndexError:
        mb.showerror("Error", "Выберите таблицу для скачивания!")
    except ValueError:
        pass


start()
