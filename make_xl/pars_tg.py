from key import API_ID, API_HASH
from typing import AsyncGenerator
from pyrogram.types import Message
from pyrogram import Client
from json import dump
import asyncio
from os import getcwd
from logging import getLogger

logger = getLogger(__name__)
"""
    CopyContent - скачивает фото с телеграмм каналов у которых есть описание. И создает json file, 
    где key - номер сообщения, value - описание. Имя каждого фото соответствует kye в js file.
"""


class CopyContent:
    def __init__(self):
        self.data = {}
        self.__cwd = getcwd()
        self.__client = Client(name='my_session', api_id=API_ID, api_hash=API_HASH, phone_number='+79581110752')

    async def copy_content(self, donor_channel: int, lim: int) -> dict:
        """
            Парсер данных с каналов.
            Принимает:
                donor_channel - id канало с которого берутся данные
                lim - число сообщений для обработки
        """
        await self.__client.start()
        messages: AsyncGenerator[Message, None] = self.__client.get_chat_history(chat_id=donor_channel, limit=lim)
        async for i in messages:
            print(i)
            cap = i.caption
            iid = i.id
            if cap:
                path = self.__cwd + f'\\data_xl\\photo\\{iid}.jpeg'
                await self.__client.download_media(message=i, file_name=path)
                self.data[f"{iid}"] = str(cap)
                logger.info(f"Добавление товара {cap}")

        return self.data

    async def deleting(self, lim):
        data = {"Кресла": [], "КАБИНЕТЫ ДИРЕКТОРА": [], "СТОЛЫ ПРЯМЫЕ": [], "СТОЛЫ УГЛОВЫЕ": [], "СТУЛЬЯ": []}
        await self.__client.start()
        messages: AsyncGenerator[Message, None] = self.__client.get_chat_history(chat_id=-1001725812699, limit=lim)
        async for i in messages:
            logger.info(f"Проверка сообщения {i}")
            title = i.forward_from_chat.title
            print(title)
            if title in data.keys():
                cap = i.caption
                # print(title, cap)
                if cap:
                    data[title].append(cap)
                    logger.info(f"Добавление в очередь на удаление {cap}")

        return data

    def dump_data(self) -> None:
        """
            Загрузка данных в json file
        """
        with open(f"{self.__cwd}/data_xl/captions", "w") as f:
            dump(self.data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    channels = {"straight tables": -1001166492970,
                "comp armchair": -1001198770422,
                "cabinet": -1001216807024,
                "closet": -1001390310467,
                "director office": -1001479107169,
                "corner tables": -1001492485587,
                "chairs": -1001430077633}
    copytables = CopyContent()
    # asyncio.run(copytables.copy_content(-1001725812699, 10))
    print(asyncio.run(copytables.deleting(46)))

    copytables.dump_data()
