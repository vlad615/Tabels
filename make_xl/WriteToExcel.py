from re import search, findall
from random import choice
from pars_tg import CopyContent
from UrlPhoto import asc_url
from add_data import AddData
from avitodata import set_id, set_address
import pandas as pd
from json import load
import asyncio
from os import getcwd, scandir, remove

# import uvloop

"""
    class LoadData
        Запускает парсер телеграмма и загружает данные в таблицу.

    При создании принимает 2 аргумента:
        choose - имя телеграмм канала: straight tables, comp armchair, cabinet, closet, director office, corner tables,
            chairs.
        count_mass - количество фото,которое должно войти в парсинг
"""


class LoadData:
    _channels = {"straight tables": -1001166492970,
                 "comp armchair": -1001198770422,
                 "cabinet": -1001216807024,
                 "closet": -1001390310467,
                 "director office": -1001479107169,
                 "corner tables": -1001492485587,
                 "chairs": -1001430077633}
    __cwd = getcwd()
    main_text = ["""Для того, чтобы получить больше предложений и подобрать мебель под ваши личные нужды напишите или позвоните нам---->
    🔥 Система больших скидок действует при опте и в праздничные дни 
    ✔ Самовывоз
    ✔Оплата наличными или безнал. Перевод на карту. Система быстрых платежей. 
    ➕ Адрес: Склад в г. Одинцово улица Старое Яскино 75ст2. Ориентир ворота с вывеской Офис Комфорт
    ➕ При поиске нас в навигаторе наберите – 
    Офис комфорт Одинцово 
    ➕ Наш телеграмм канал – office comfort es
    🕒 График: Часы работы склада с 10 до 19, Выходной Вс. 
    -------------------------------------------------------------------
    Oфис Комфорт — это большой склад офисной мебели, после закрытия больших организаций, в городе Одинцово М.О.
    На нашем складе вы найдете мебель на любой вкус. У много как дешевой бу мебели, так и мебель известных производителей представительного класса. 
    Работаем уже 6 лет, развиваясь и улучшая сервисный центр
    Можем укомплектовать 100-200 рабочих мест.
    """, """Для того, чтобы получить больше предложений и подобрать мебель под ваши личные нужды напишите или позвоните нам---->
            ➕ Адрес: Склад в г. Одинцово улица Старое Яскино 75ст2. Ориентир ворота с вывеской Офис Комфорт
            ➕ При поиске нас в навигаторе наберите – 
            Офис комфорт Одинцово 
            ➕ Наш телеграмм канал – office comfort es
            🕒 График: Часы работы склада с 10 до 19, Выходной Вс. 
            -------------------------------------------------------------------
            Oфис Комфорт — это большой склад офисной мебели, после закрытия больших организаций, в городе Одинцово М.О.
            На нашем складе вы найдете мебель на любой вкус. У много как дешевой бу мебели, так и мебель известных производителей представительного класса. 
            Работаем уже 6 лет, развиваясь и улучшая сервисный центр
            Можем укомплектовать 100-200 рабочих мест."""]
    add_text = {
        "comp armchair": """
    В наличии более 150 разных компьютерных кресел бу для работы дома и в офисе.
    Вы можете написать нашим менеджерам, что бы подобрать под свои личные параметры и в нужном количестве.
    """,

        "tables": """
    У нас на складе имеются столы для работы дома и в офисе, самых разных размеров и видов. 
    В наличии более 300 столов, которые хранятся на складе в разобранном виде. 
    Есть презентабельные столы для элитных офисов до 15 000 и простые для домашнего использования от 999. 
    К столам можем подобрать тумбы, кресла и шкафы.
    """,

        "closet": """
    Широкий ассортимент офисных шкафов для одежды и стеллажей для докуменетов, в разном исполнении материала и декоров. 
    Все шкафы собраны и доступны для осмотра и оценки состояния. 
    Можем подобрать к шкафу компьютерное кресло или стул с письменным столом, 
    дополнительно в магазине большой выбор тумб для оргтехники, выкатных тумб на колесиках и приставных тумб к столу.
    Шкафы для документов 2499
    Гардеробы от 4499р
    Шкафы с небольшими изъянами и открытые стеллажи от 2499р
    Железный с полочками 9999
    """,

        "cabinet": """
    Офисная тумба на колёсиках 
    У нас есть много тумб, которые подойдут офиса и дома. Все тумбы бу в хорошем состоянии за 1999.
    Но так же имеются тумбы с изъянами за 999 руб. 
    Есть металлические тумбы и картотеки от 2999
    """,

        "chairs": """
    В нашем магазине вы найдете стулья для любой цели использования. 
    Удобные стулья-кресла для конференций или обычные изо стулья в офис, 
    так же есть стулья для кухни разных цветов, для любого интерьера. 
    Самая низкая цена стула 799
    """}
    _tables_field = {
        'cabinet': [['GoodsType', 'GoodsSubType', 'DresserType', 'Material', 'FurnitureAdditions', "Color"],
                    ['Шкафы, комоды и стеллажи', 'Комоды и тумбы', 'Тумба']],
        'chairs': [['GoodsType', 'GoodsSubType', 'SeatMaterial', 'BaseMaterial', 'FurnitureAdditions', "Color"],
                   ['Столы и стулья', 'Стулья']],

        'closet': [['GoodsType', 'GoodsSubType', 'CabinetType', 'Material', 'Purpose', "Color"],
                   ['Шкафы, комоды и стеллажи', 'Шкафы и буфеты', "Шкаф"]],

        'comp armchair': [['GoodsType', 'GoodsSubType', 'DeskChairType', 'ComputerChairType', 'UpholsteryMaterial',
                           'FurnitureAdditions', "Color"],
                          ['Компьютерные столы и кресла', 'Кресла и стулья', 'Компьютерные кресла', 'Компьютерное']],
        'straight tables': [['GoodsType', 'GoodsSubType', 'FoldingMechanism', 'TableType', 'FurnitureShape',
                             'TabletopMaterial', 'BaseMaterial', 'FurnitureAdditions', 'Purpose', "Color"],
                            ['Столы и стулья', 'Столы', 'Нет']],
        'corner tables': [['GoodsType', 'GoodsSubType', 'FoldingMechanism', 'TableType', 'FurnitureShape',
                           'TabletopMaterial', 'BaseMaterial', 'FurnitureAdditions', 'Purpose', "Color"],
                          ['Столы и стулья', 'Столы', 'Нет']],
        'director office': [['GoodsType', 'GoodsSubType', 'FoldingMechanism', 'TableType', 'FurnitureShape',
                             'TabletopMaterial', 'BaseMaterial', 'FurnitureAdditions', 'Purpose', "Color"],
                            ['Столы и стулья', 'Столы', 'Нет']]

    }

    __content = CopyContent()

    def __init__(self, choose: str):
        self.choose = choose

    @classmethod
    def __open_xl(cls, name_table: str) -> pd.DataFrame:
        """
            Открытие таблицы и чтение с нее данных в ДатаФрейм.

            Принимает:
                name_table = self.choose
            Возвращает:
                DataFrame - данные из таблицы дозаполнения
                name - название открытой таблицы:
                    для Директорской, угловых и прямых столов - tables
                    для остальных self.choose
        """

        pass

    @classmethod
    def __read_js(cls):
        """
            Открывает файл с запарсенными данными и передает их
        """
        try:
            with open(f"{cls.__cwd}/data_xl/captions", "r") as f:
                cont = load(f)
                return cont
        except FileNotFoundError:
            return "This file doesn`t exist"

    @classmethod
    def __load_data_xl(cls, name: str) -> None:
        """
            Запускает функцию загрузки данных и добавляет фото в таблицу
            Принимает
                name - self.choose
        """
        pars_data = cls.__read_js()
        xl = pd.read_excel(f"{cls.__cwd}/data_xl/{name}.xlsx")
        fr = pd.DataFrame(xl)
        key = list(pars_data.keys())
        field = ['Title', 'Description', 'Price', 'ImageUrls', 'Id', 'VideoURL', 'Category', 'AdType', 'Condition',
                 'Availability']
        field.extend(cls._tables_field[name][0])

        for i in key:
            title = search(r"(.*)", pars_data[i]).group()
            description = pars_data[i] + "\n" + (
                cls.add_text[name] if name in cls.add_text else cls.add_text['tables']) + "\n" + choice(cls.main_text)
            price = findall(r"Цена[: ]?([\d ]*)", pars_data[i]) or ['']
            art = findall(r"[Аa]рт(?:икул)?[. (]*([\d]*)", pars_data[i]) or [1]
            image_url = asc_url(i)

            data_add = None
            if name in ("straight tables", "corner tables", "director office"):
                size = map(int, findall(r'(\d{2,3})[хx/\\](\d{2,3})[хx/\\](\d{2,3})', pars_data[i])[0])
                data_tab = AddData("tables", i)
                data_add = data_tab.data
                data_add.extend(size)
                field.extend(['Length', 'Width', 'Height'])
            elif name == 'comp armchair':
                data_comp = AddData("comp_armchair", i)
                data_add = data_comp.data
            elif name == "closet":
                size = map(int, findall(r'(\d{2,3})[хx/\\](\d{2,3})[хx/\\](\d{2,3})', pars_data[i])[0])
                data_cab = AddData("closet", i)
                data_add = data_cab.data
                data_add.extend(size)
                field.extend(('Width', 'Depth', 'Height'))
            elif name == "chairs":
                data_comp = AddData("chairs", i)
                data_add = data_comp.data
            else:
                size = map(int, findall(r'(\d{2,3})[хx/\\](\d{2,3})[хx/\\](\d{2,3})', pars_data[i])[0])
                data_cab = AddData("cabinet", i)
                data_add = data_cab.data
                data_add.extend(size)
                field.extend(('Width', 'Depth', 'Height'))

            lst = [title, description, int(price[0].replace(' ', '')), image_url, int(art[0]),
                   'https://youtu.be/ycYx204IpKc?si=5z8-v1fOQP2SdfR_', 'Мебель и интерьер',
                   'Товар приобретен на продажу', 'Б/у', 'В наличии']

            lst.extend(cls._tables_field[name][1])
            lst.extend(data_add)

            fr.loc[len(fr.index), field] = lst

        fr.to_excel(f"{cls.__cwd}/data_xl/{name}.xlsx", index=False)

    def table_for_avito(self):
        fr = self.__open_xl(self.choose)
        index = fr["Address"].isnull().sum()
        start_id = len(fr.index) - index
        ides = set_id(index)
        address, file = set_address(index)

        for i in range(index):
            fr.loc[start_id, ["Id", "Address"]] = [ides[i], address[i]]
            start_id += 1

        fr.to_excel(file, index=False)

    @classmethod
    def __end_program(cls) -> None:
        """
            Завершение программы - удаление скачаных фото
        """
        pat = f"{cls.__cwd}/data_xl/photo"
        files = scandir(pat)
        for i in files:
            remove(i)

    def start_pars(self, count_mass: int):
        """
            Запуск парсера
            Загрузка текста в файл
            Запуск загрузки данных в эксель таблицу
            Удаление фото
        """
        # uvloop.install()
        asyncio.run(self.__content.copy_content(self._channels[self.choose], count_mass))
        self.__content.dump_data()
        self.__load_data_xl(self.choose)
        self.__end_program()


if __name__ == "__main__":
    x = LoadData("chairs")
    # # x.start_pars(8)
    # x.table_for_avito()
