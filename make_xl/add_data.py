from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox as mb


class AddData:

    def __init__(self, table: str, photo: str):
        colors = ["Бежевый", "Белый", "Бирюзовый", "Бордовый", "Голубой", "Жёлтый", "Зелёный", "Коричневый", "Красный",
                  "Оранжевый", "Розовый", "Серебристый", "Серый", "Синий", "Фиолетовый", "Чёрный", "Разноцветный",
                  "Другой"]
        self.table = table
        self.root2 = Tk()
        self.root2.title("Укажите данные товара")
        self.canvas = Canvas(self.root2)
        self.canvas.grid(row=0, column=0, columnspan=5, stick="we")
        self.photo = ImageTk.PhotoImage(Image.open(f'./data_xl/photo/{photo}.jpeg').resize((310, 300)))
        self.canvas.create_image(0, 0, anchor=NW, image=self.photo)
        self.variables = {
            "closet": {'Material': ["МДФ", "Металл", "Пластик", "ДСП"],
                       'Purpose': ["Кабинет", "Офис", "Балкон", "Гостиная", "Прихожая", "Спальня"],
                       "Color": colors},
            "comp_armchair": {'UpholsteryMaterial': ["Искусственная кожа", "Кожа", "Ткань", "Сетка", "Замша", "Дерево"],
                              'FurnitureAdditions': ["Подлокотники", "Подголовник", "Механизм качания",
                                                     "Регулировка наклона спинки", "Регулировка высоты",
                                                     "Регулировка подлокотников", "Регулировка глубины сиденья",
                                                     "Поясничный упор"],
                              "Color": colors},
            "cabinet": {"Material": ["ЛДСП", "ДСП", "Металл", "Пластик"],
                        "FurnitureAdditions": ["Колесики", "Ящики"],
                        "Color": colors},
            "chairs": {'SeatMaterial': ["Искусственная кожа", "Кожа", "Ткань"],
                       'BaseMaterial': ["Металл", "Пластик", "Дерево"],
                       'FurnitureAdditions': ["Подлокотники", "Колёсики", "Мягкое сидение", "Мягкая спинка"],
                       "Color": colors},
            "tables": {"TableType": ["Письменный", "Кухонный", "Барный", "Журнальный", "Другой"],
                       "FurnitureShape": ["Прямоугольный", "Квадратный", "Круглый", "Овальный", "Полукруглый",
                                          "Угловой"],
                       "TabletopMaterial": ["ДСП", "ЛДСП", "Стекло", "Дерево"],
                       "BaseMaterial": ["ДСП", "Дерево", "Металл"],
                       "FurnitureAdditions": ["Тумба"],
                       "Purpose": ["Кабинет", "Кухня", "Бар/Кафе"],
                       "Color": colors}

        }[table]
        self.var = list(self.variables.keys())
        self.data = []
        width = 30 if self.table == "comp_armchair" else 17
        self.labels = [Label(self.root2) for i in self.var]
        self.lists = [
            Listbox(listvariable=Variable(value=self.variables[i]), width=width, height=len(self.variables[i]),
                    exportselection=True if i == "Color" else False,
                    selectmode=MULTIPLE if i not in ("TableType", "FurnitureShape", "SeatMaterial", "BaseMaterial",
                                                     "Color") else BROWSE)
            for i in self.var]
        self.asc()

    def tables(self):
        for i in range(len(self.var)):
            if (not ' | '.join(self.variables[self.var[i]][j] for j in self.lists[i].curselection()) and self.var[i] !=
                    "FurnitureAdditions"):
                self.data.clear()
                mb.showerror("Ошибка", """Выберите хотя бы одни эллемент в каждом параметре. 
                (Кроме FurnitureAdditions)""")
                break
            self.data.append(' | '.join(self.variables[self.var[i]][j] for j in self.lists[i].curselection()))
        else:
            self.root2.destroy()

    def cabinet(self):
        for i in range(len(self.var)):
            if not ' | '.join(self.variables[self.var[i]][j] for j in self.lists[i].curselection()):
                self.data.clear()
                mb.showerror("Ошибка", """Выберите хотя бы одни эллемент в каждом параметре.""")
                break
            self.data.append(' | '.join(self.variables[self.var[i]][j] for j in self.lists[i].curselection()))
        else:
            self.root2.destroy()

    def closet(self):
        for i in range(len(self.var)):
            if not ' | '.join(self.variables[self.var[i]][j] for j in self.lists[i].curselection()):
                self.data.clear()
                mb.showerror("Ошибка", """Выберите хотя бы одни эллемент в каждом параметре.""")
                break
            self.data.append(' | '.join(self.variables[self.var[i]][j] for j in self.lists[i].curselection()))
        else:
            self.root2.destroy()

    def comp_armchair(self):
        for i in range(len(self.var)):
            if not ' | '.join(self.variables[self.var[i]][j] for j in self.lists[i].curselection()):
                self.data.clear()
                mb.showerror("Ошибка", """Выберите хотя бы одни эллемент в каждом параметре.""")
                break
            self.data.append(' | '.join(self.variables[self.var[i]][j] for j in self.lists[i].curselection()))
        else:
            self.root2.destroy()

    def chairs(self):
        for i in range(len(self.var)):
            if not ' | '.join(self.variables[self.var[i]][j] for j in self.lists[i].curselection()):
                self.data.clear()
                mb.showerror("Ошибка", """Выберите хотя бы одни эллемент в каждом параметре.""")
                break
            self.data.append(' | '.join(self.variables[self.var[i]][j] for j in self.lists[i].curselection()))
        else:
            self.root2.destroy()

    def asc(self):
        for i in range(len(self.var)):
            self.labels[i].config(text=self.var[i])
            self.labels[i].grid(column=0 + i, row=1)
            self.lists[i].grid(column=0 + i, row=2)
        but = Button(self.root2, text="Отправить", command=self.__getattribute__(f"{self.table}"), width=20, )
        but.grid(column=1, pady=10, stick='w')

        self.root2.resizable(False, False)
        self.root2.mainloop()


if __name__ == "__main__":
    g = AddData("comp_armchair", "522")
    print(g.data)
