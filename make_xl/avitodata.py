from random import randint, shuffle
from tkinter import filedialog


def set_id(count_id: int) -> list[int]:
    start_id = randint(1_000, 1_000_000)
    ids = []

    for i in range(count_id):
        ids.append(start_id)
        start_id += 1

    return ids


def set_address(cont_id: int) -> tuple[list[str], str]:
    addresses = ["Москва, Беловежская улица", "Москва, Часовая улица", "Москва, 7-я Парковая улица",
                 "Москва, Чертановская улица", "Московская область, Одинцово", "Московская область, Химки",
                 "Московская область, Подольк", "Московская область, Балашиха"]

    if cont_id // 8:
        addresses = addresses * (cont_id // 8 + 1)
    shuffle(addresses)

    filepath = filedialog.asksaveasfilename(filetypes=(('Excel files', '*.xlsx'), ), initialfile="avito_table")
    return addresses[:cont_id], filepath


if __name__ == "__main__":
    assert len(set_id(15)) == 15
    assert len(set_address(1)) == 1
    assert set_address(15) == 15
    assert set_address(40) == 40
    assert set_address(25) == 25
    assert set_address(17) == 17
    assert set_address(10) == 10
    assert set_address(8) == 8
    assert set_address(5) == 5
