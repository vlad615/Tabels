from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox as mb


def asc_cab_data(path_photo: str, fields: list) -> list:
    root2 = Tk()
    root2.title("Укажите данные товара")
    canvas = Canvas(root2)
    canvas.grid(row=0, column=0, columnspan=5, stick="we")
    photo = ImageTk.PhotoImage(Image.open(f'./data_xl/photo/{path_photo}.jpeg').resize((310, 300)))
    canvas.create_image(0, 0, anchor=NW, image=photo)
    variables = {"Material": ["ЛДСП", "ДСП", "Металл", "Пластик"],
                 "FurnitureAdditions": ["Колесики", "Ящики"],
                 "Color": ["Бежевый", "Белый", "Бирюзовый", "Голубой", "Жёлтый", "Зелёный", "Коричневый", "Красный",
                           "Оранжевый", "Розовый", "Серебристый", "Серый", "Синий", "Фиолетовый", "Чёрный",
                           "Разноцветный", "Другой"]}
    data = []

    labels = [Label(root2) for i in fields]
    lists = [Listbox(listvariable=Variable(value=variables[i]), height=len(variables[i]),
                     exportselection=True if i == "Color" else False, selectmode=MULTIPLE if i != "Color" else BROWSE)
             for i in fields]

    for i in range(len(fields)):
        labels[i].config(text=fields[i])
        labels[i].grid(column=0+i, row=1)
        lists[i].grid(column=0+i, row=2)

    def check():
        for i in range(len(fields)):
            if not ' | '.join(variables[fields[i]][j] for j in lists[i].curselection()):
                data.clear()
                mb.showerror("Ошибка", "Выберите хотя бы одни эллемент в каждом параметре.")
                break
            data.append(' | '.join(variables[fields[i]][j] for j in lists[i].curselection()))
        else:
            root2.destroy()

    but = Button(root2, text="Отправить", command=check, width=20, )
    but.grid(column=1, pady=10, stick='w')

    root2.resizable(False, False)
    root2.mainloop()
    return data


if __name__ == "__main__":
    asc_cab_data("439", ['Material', 'FurnitureAdditions', "Color"])
