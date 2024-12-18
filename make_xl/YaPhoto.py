import yadisk
from key import APL_ID, APL_SCR, YA_TOKEN
from logging import getLogger

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
                client.publish(path)
            if i.name.startswith(str(art)):
                urls.append(i.public_url)
    logger.info(f"{len(urls)} ссылок добавлено")
    return " | ".join(urls)


if __name__ == "__main__":
    g = get_url("director office", 121)
    print(g)
    print(len(g))
