from re import search, findall
from random import choice
from pars_tg import CopyContent
from UrlPhoto import asc_url
from cab_data import asc_cab_data
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
    _colors = {"Бежевый": "Бежевый",
               "Белый": "Белый",
               "Бирюзовый": "Бирюзовый",
               "Голубой": "Голубой",
               "Жёлтый": "Жёлтый",
               "Зелёный": "Зелёный",
               "Коричневый": "Коричневый",
               "Красный": "Красный",
               "Оранжевый": "Оранжевый",
               "Розовый": "Розовый",
               "Серебристый": "Серебристый",
               "Серый": "Серый",
               "Синий": "Синий",
               "Фиолетовый": "Фиолетовый",
               "Чёрный": "Чёрный",
               "Разноцветный": "Разноцветный",
               "Другой": "Другой",
               }
    _tables_field = {
        'main': [['VideoURL', 'Category', 'AdType', 'Condition', 'Availability'],
                 ['https://youtu.be/ycYx204IpKc?si=5z8-v1fOQP2SdfR_', 'Мебель и интерьер', 'Товар приобретен на продажу',
                  'Б/у', 'В наличии']],
        'cabinet': [['GoodsType', 'GoodsSubType', 'DresserType'],
                    ['Шкафы, комоды и стеллажи', 'Комоды и тумбы', 'Тумба']],
        'chairs': [['GoodsType', 'GoodsSubType'], ['Столы и стулья', 'Стулья']],

        'closet': [['GoodsType', 'GoodsSubType', 'CabinetType'],['Шкафы, комоды и стеллажи', 'Шкафы и буфеты', "Шкаф"]],

        'comp armchair': [['GoodsType', 'GoodsSubType', 'DeskChairType', 'ComputerChairType'],
            ['Компьютерные столы и кресла', 'Кресла и стулья', 'Компьютерные кресла', 'Компьютерное']],
        'tables': [['GoodsType', 'GoodsSubType', 'FoldingMechanism'], ['Столы и стулья', 'Столы', 'Нет']]
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


        return data_f

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
    def __load_cabinet_data(cls, cap, photo, field_add) -> pd.DataFrame:
        width, depth, height = findall(r'(\d{2,3})[хx/\\](\d{2,3})[хx/\\](\d{2,3})', cap)[0]
        data_cab = asc_cab_data(photo, field_add)
        field_add.extend(('Width', 'Height', 'Depth'))

        return field_add

    @classmethod
    def __load_chairs_data(cls, frame: pd.DataFrame, pars: dict, key: list, ind: int) -> pd.DataFrame:
        index = ind

        for i in key:
            width, depth, height = findall(r'(\d{2,3})[хx/\\](\d{2,3})[хx/\\](\d{2,3})', pars[i])[0]
            frame.loc[index, ['Width', 'Height', 'Depth']] = [int(width), int(height), int(depth)]
            index += 1

        return frame

    @classmethod
    def __load_closet_data(cls, frame: pd.DataFrame, pars: dict, key: list, ind: int) -> pd.DataFrame:
        index = ind

        for i in key:
            width, depth, height = findall(r'(\d{2,3})[хx/\\](\d{2,3})[хx/\\](\d{2,3})', pars[i])[0]
            frame.loc[index, ['Width', 'Height', 'Depth']] = [int(width), int(height), int(depth)]
            index += 1

        return frame

    @classmethod
    def __load_armchair_data(cls, frame: pd.DataFrame, pars: dict, key: list, ind: int) -> pd.DataFrame:
        index = ind
        for i in key:
            try:
                sizes = findall(r'(\d{2,3})[хx/\\](\d{2,3})', pars[i])
                width, depth = sizes[0]
                maxh, minh = sizes[1]
                frame.loc[index, ['Width', 'Depth', 'MaxHeight', 'MinHeight']] = [width, depth, maxh, minh]
            except IndexError:
                pass
            else:
                width, depth, maxh, minh = 48, 50, 45, 57
                frame.loc[index, ['Width', 'Depth', 'MaxHeight', 'MinHeight']] = [width, depth, maxh, minh]

        return frame

    @classmethod
    def __load_tables_data(cls, frame: pd.DataFrame, pars: dict, key: list, ind: int) -> pd.DataFrame:
        index = ind
        for i in key:
            length, width, height = findall(r'(\d{2,3})[хx/\\](\d{2,3})[хx/\\](\d{2,3})', pars[i])[0]
            frame.loc[index, ['Width', 'Height', 'Length']] = [int(width), int(height), int(length)]
            index += 1

        return frame

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
        ind = len(fr.index)
        field = ['Title', 'Description', 'Price', 'ImageUrls', 'Id']
        field.extend(cls._tables_field['main'][0])
        field.extend(cls._tables_field[name][0])

        for i in key:
            title = search(r"(.*)", pars_data[i]).group()
            description = pars_data[i] + "\n" + (
                cls.add_text[name] if name in cls.add_text else cls.add_text['tables']) + "\n" + choice(cls.main_text)
            price = findall(r"Цена[: ]?([\d ]*)", pars_data[i]) or ['']
            art = findall(r"[Аa]рт(?:икул)?[. (]*([\d]*)", pars_data[i]) or [1]
            image_url = asc_url(i)

            field_add, data_add = None, None
            if name in ("straight tables", "corner tables", "director office"):
                field_add = ['TableType', 'FurnitureShape', 'TabletopMaterial', 'BaseMaterial', 'FurnitureAdditions',
                             'Purpose', "Color"]
                field_add, data_add = cls.__load_tables_data(pars_data[i], i, field_add)
            elif name == 'comp armchair':
                field_add = ['UpholsteryMaterial', 'FurnitureAdditions']
                field_add, data_add = cls.__load_armchair_data(pars_data[i], i, field_add)
            elif name == "closet":
                field_add = ['Material', 'Purpose', "Color"]
                field_add, data_add = cls.__load_closet_data(pars_data[i], i, field_add)
            elif name == "chairs":
                field_add = ['SeatMaterial', 'BaseMaterial', 'FurnitureAdditions', "Color"]
                field_add, data_add = cls.__load_chairs_data(pars_data[i], i, field_add)
            else:
                field_add = ['Material', 'FurnitureAdditions', "Color"]
                data_add = cls.__load_cabinet_data(pars_data[i], i, field_add)

            lst = [title, description, int(price[0].replace(' ', '')), image_url, int(art[0])]
            lst.extend(cls._tables_field['main'][1])
            lst.extend(cls._tables_field[name][1])

            fr.loc[len(fr.index), field] = lst

        fr.to_excel(name + '.xlsx', index=False)

    def table_for_avito(self):
        fr = self.__open_xl(self.choose)
        index = fr["Id"].isnull().sum()
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
