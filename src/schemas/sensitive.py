"""_summary_
"""
from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Dict

from fastapi import Query
from khayyam import JalaliDatetime

current_date = JalaliDatetime.today().replace(day=1).strftime("%Y-%m-%d")
current_month = JalaliDatetime.today().month
current_year = JalaliDatetime.today().year
from datetime import date

current_date = (
    date.today().isoformat()
)  # JalaliDatetime.today().replace(day=1).strftime("%Y-%m-%d")


@dataclass
class ResponseListOut:
    result: Dict
    timeGenerated: JalaliDatetime
    error: str = Query("nothing")


@dataclass
class Pages:
    size: int = Query(10, alias="PageSize")
    page: int = Query(1, alias="PageNumber")


class SensitiveTypeEnum(str, Enum):
    Hack = "Hack"
    Other = "Other"


class SensitiveCategoryEnum(str, Enum):
    Rule = "Rule"
    Other = "Other"


class SortOrder(IntEnum):
    ASCENDING = 1
    DESCENDING = -1


@dataclass
class AddSensitiveIn:
    SensitiveID: str
    SensitiveType: SensitiveTypeEnum = Query(
        SensitiveTypeEnum.Other, alias="SensitiveType"
    )
    SensitiveCategory: SensitiveCategoryEnum = Query(
        SensitiveCategoryEnum.Other, alias="SensitiveCategory"
    )
    Word: str = None
    Description: str = None
    # AddDate: str = None


@dataclass
class ModifySensitiveIn:
    SysSensitiveID: str
    SensitiveID: str
    SensitiveType: SensitiveTypeEnum = Query(
        SensitiveTypeEnum.Other, alias="SensitiveType"
    )
    SensitiveCategory: SensitiveCategoryEnum = Query(
        SensitiveCategoryEnum.Other, alias="SensitiveCategory"
    )
    Word: str = None
    Description: str = None
    AddDate: str = None
    SensitiveNumber: str = None


@dataclass
class SearchSensitiveIn:
    SensitiveID: str = Query(None)
    SysSensitiveID: str = None
    SensitiveNumber: str = None
    Description: str = None
    SensitiveType: SensitiveTypeEnum = Query(
        SensitiveTypeEnum.Other, alias="SensitiveType"
    )
    SensitiveCategory: SensitiveCategoryEnum = Query(
        SensitiveCategoryEnum.Other, alias="SensitiveCategory"
    )
    Word: str = None
    AddDate: str = None
    size: int = Query(10, alias="PageSize")
    page: int = Query(1, alias="PageNumber")


@dataclass
class DelSensitiveIn:
    SysSensitiveID: str
