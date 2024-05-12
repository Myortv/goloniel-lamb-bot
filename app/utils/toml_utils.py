
from pydantic import BaseModel

import toml


class FromTomlFile(BaseModel):
    def __init__(self, path: str, *args, **kwargs):
        with open(path, 'r') as file:
            loaded_data = toml.load(file).get(self.__class__.__name__)
            return super().__init__(**loaded_data)
