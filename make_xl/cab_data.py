from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox as mb


def asc_cab_data(path_photo: str, fields: list) -> str:
    root2 = Tk()
    root2.title("Укажите данные товара")
    canvas = Canvas(root2)
    canvas.grid(row=0, column=0, columnspan=5, stick="we")
    photo = ImageTk.PhotoImage(Image.open(f'./data_xl/photo/{path_photo}').resize((310, 300)))  # .jpeg
    canvas.create_image(0, 0, anchor=NW, image=photo)
    variables = {"Material": ["ЛДСП", "ДСП", "Металл", "Пластик"],
                 "FurnitureAdditions": ["Колесики", "Ящики"],
                 "Color": ["Бежевый", "Белый", "Бирюзовый", "Голубой", "Жёлтый", "Зелёный", "Коричневый", "Красный",
                           "Оранжевый", "Розовый", "Серебристый", "Серый", "Синий", "Фиолетовый", "Чёрный",
                           "Разноцветный", "Другой"]}
    urls = []
    union_url: str = ""

    labels = [Label(root2) for i in fields]
    lists = [Checkbutton(text=f"{j}") for n in fields for j in variables[n]]
    for i in range(len(fields)):
        labels[i].configure(text=f"{fields[i]}")
        labels[i].grid(row=i + 1, column=0, pady=3, stick="e")
        for j in
        lists[i].grid(row=i + 1, column=1, pady=3, stick="w")

    def check():
        for i in variables.keys():
            print()

    but = Button(root2, text="Отправить", command=check, width=20, )
    but.grid(column=1, pady=10, stick='w')

    root2.resizable(False, False)
    root2.mainloop()
    return union_url


if __name__ == "__main__":
    asc_cab_data("IMG_20230208_160750.jpg", ['Material', 'FurnitureAdditions', "Color"])
