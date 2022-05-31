# import standard modules
from __future__ import annotations
from typing import Optional, List, Dict


# import third party modules
from pydantic import BaseModel

# from project related modules


class RowMask(BaseModel):
    columnName: str
    valueName: str
    replaceType: str
    customReplaceValue: str
    visible: bool

    def getattr(self, item):
        try:
            return self.__getattribute__(item)
        except AttributeError:
            return None


class ColumnMask(BaseModel):
    columnName: str
    replaceType: str
    visible: bool

    def getattr(self, item):
        try:
            return self.__getattribute__(item)
        except AttributeError:
            return None


class MaskingObject(BaseModel):
    name: str
    table: str
    groups: List[Dict[str, str]]
    rows: Optional[List[RowMask]]
    columns: Optional[List[ColumnMask]]


class DataBaseConfig(BaseModel):
    name: str
    host: str
    port: str
    user: str
    password: str
    database: str
    databaseSchema: str
    connectorName: str
    valid: bool = True
