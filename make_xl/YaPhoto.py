import yadisk
from key import APL_ID, APL_SCR, YA_TOKEN
from logging import getLogger
from tkinter.messagebox import showerror
logger = getLogger(__name__)

client = yadisk.Client(id=APL_ID, secret=APL_SCR, token=YA_TOKEN)

paths = {'cabinet': "Тумбы",
         'chairs': "Стул",
         'closet': "Шкафы",
         'comp armchair': "Кресло",
         'straight tables': "Столы",
         'corner tables': "Столы угловые",
         'director office': "Кабинет руководителя"}


def get_url(folder: str, art: int):
    path = f"/Мебель/{paths[folder]}"

    urls = []
    with client:
        for i in list(client.listdir(path)):
            if not i.public_url:
                logger.info(f"publish {i.name}")
                client.publish(path+"/"+i.name)

        for i in list(client.listdir(path)):
            if i.name.startswith(str(art)):
                logger.info(f"add {i.public_url}")
                urls.append("https://disk.yandex.ru/i/" + i.public_url[-14:])
    if urls:
        logger.info(f"{len(urls)} ссылок добавлено")
        return " | ".join(urls)
    else:
        showerror("Ошибка поиска фото", "Проверьте правильно ли добавлены фото в ЯДиск!")
        get_url(folder, art)


if __name__ == "__main__":
    g = get_url("straight tables", 25)
    print(g)
