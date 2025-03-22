import tkinter
from tkinter import *
from pars_tg import CopyContent
import asyncio
from WriteExcel import LoadData, ChangeTabel
# import uvloop
from tkinter import font
from tkinter import messagebox as mb
from functools import wraps
from logging import getLogger, basicConfig, INFO, DEBUG


logger = getLogger()
FORMAT = "%(name)s : %(levelname)s : %(message)s"
basicConfig(level=INFO, format=FORMAT)


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

    vals = {"Прямые столы": ("straight tables", -1001166492970),
            "Угловые столы": ("corner tables", -1001492485587),
            "Директорская мебель": ("director office", -1001479107169),
            "Компьютерные кресла": ("comp armchair", -1001198770422),
            "Стулья": ("chairs", -1001430077633),
            "Шкафы": ("closet", -1001390310467),
            "Тумбы": ("cabinet", -1001216807024), }

    main_menu = tkinter.Menu()
    menu = tkinter.Menu()
    menu.add_command(label="Удалить проданные товары", command=lambda: delete_goods(enter_count.get()))
    menu.add_command(label="Скачать исходную таблицу", command=lambda: add_goods(vals[key[listbox.curselection()[0]]],
                                                                       enter_count.get(), root))
    menu.add_command(label="Заменить таблицу", command=lambda: add_goods(vals[key[listbox.curselection()[0]]],
                                                                       enter_count.get(), root))
    menu.add_separator()
    menu.add_command(label="Инструкция", command=lambda: add_goods)
    main_menu.add_cascade(label="Меню", menu=menu)
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

    # but_delete = Button(text="Удалить проданые", command=lambda: delete_goods(enter_count.get()))

    listbox.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)
    label.grid(row=1, column=0, columnspan=2, sticky="w", padx=3, pady=5)
    enter_count.grid(row=2, column=0, columnspan=2, sticky="w", padx=3, pady=5)
    but_pars.grid(row=3, column=0, sticky="w", padx=3, pady=5)
    but_download.grid(row=3, column=1, sticky="w", padx=3, pady=5)
    # but_delete.grid(row=3, column=1, sticky="e", padx=3, pady=5)
    root.config(menu=main_menu)
    root.mainloop()


def delete_goods(count: str):
    if not count.isdigit():
        mb.showerror('Error', "Введите количество сообщений для обработки")
    else:
        logger.info(f"Запуск обновления таблиц")
        content = CopyContent()

        # uvloop.install()
        asyncio.run(content.deleting(int(count)))
        content.dump_data()
        data = LoadData()
        data.start_del()


@event
def add_goods(channel: tuple, con: str, root):
    try:
        if not con.isdigit():
            mb.showerror('Error', "Введите количество сообщений для обработки")
        else:
            logger.info(f"Запуск программы добавления в таблицу {channel}")
            content = CopyContent()

            # uvloop.install()
            asyncio.run(content.copy_content(channel[1], int(con)))
            content.dump_data()
            data = LoadData(channel[0])
            root.destroy()
            data.start_dump()
    except IndexError:
        mb.showerror("Error", "Выберите канал для скачивания данных!")


def download(channel):
    try:
        logger.info(f"Скачивание таблицы {channel}")
        data = ChangeTabel(channel[0])
        data.table_for_avito()
    except IndexError:
        mb.showerror("Error", "Выберите таблицу для скачивания!")
    except ValueError:
        pass


start()

# if __name__=="__main__":
#     start()
