from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox as mb


def asc_url(path_photo: str, ) -> str:
    root2 = Tk()
    root2.title("Укажите ссылки на фото")
    canvas = Canvas(root2)
    canvas.grid(row=0, column=0, columnspan=5, stick="we")
    photo = ImageTk.PhotoImage(Image.open(f'./data_xl/photo/{path_photo}.jpeg').resize((310, 300)))
    canvas.create_image(0, 0, anchor=NW, image=photo)
    urls = []
    union_url: str = ""

    label = [Label(root2) for i in range(10)]
    entry = [Entry(root2, width=40) for i in range(10)]
    for i in range(10):
        label[i].configure(text=f"{i+1}: ")
        label[i].grid(row=i+1, column=0, pady=3, stick="e")
        entry[i].grid(row=i+1, column=1, pady=3, stick="w")

    def check():
        for i in entry:
            if i.get():
                urls.append(i.get())
        if len(urls) != len(set(urls)):
            urls.clear()
            mb.showerror("Вы указали повторяющиеся ссылки!\nЗамените их.")
        else:
            nonlocal union_url
            root2.destroy()
            union_url = ' | '.join(urls)

    but = Button(root2, text="Отправить", command=check, width=20, )
    but.grid(column=1, pady=10, stick='w')

    root2.resizable(False, False)
    root2.mainloop()
    return union_url


if __name__ == "__main__":
    asc_url("None", '1390')
