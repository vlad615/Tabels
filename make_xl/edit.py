import re

import pandas as pd
from os import scandir
from re import sub, search

tables = [i.name for i in scandir("data_xl") if ".xlsx" in i.name]

for name in tables:
    table = pd.read_excel('data_xl/' + name)
    for i in range(table.index.size):
        desc = table.loc[i, "Description"]
        print(i, len(desc))
        if re.search(r"\n➕ Наш телеграмм канал – office comfort es", desc):
            table.loc[i, "Description"] = sub(r"\n➕ Наш телеграмм канал – office comfort es", "", desc)

    table.to_excel("data_xl/"+name, index=False)
