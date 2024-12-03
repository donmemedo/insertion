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


class ForbiddenTypeEnum(str, Enum):
    Insulation = "Insulation"
    Other = "Other"


class ForbiddenCategoryEnum(str, Enum):
    Rule = "Rule"
    Other = "Other"


class SortOrder(IntEnum):
    ASCENDING = 1
    DESCENDING = -1


@dataclass
class AddForbiddenIn:
    ForbiddenID: str
    ForbiddenType: ForbiddenTypeEnum = Query(
        ForbiddenTypeEnum.Other, alias="ForbiddenType"
    )
    ForbiddenCategory: ForbiddenCategoryEnum = Query(
        ForbiddenCategoryEnum.Other, alias="ForbiddenCategory"
    )
    Word: str = None
    Description: str = None


@dataclass
class ModifyForbiddenIn:
    SysForbiddenID: str
    ForbiddenID: str
    ForbiddenType: ForbiddenTypeEnum = Query(
        ForbiddenTypeEnum.Other, alias="ForbiddenType"
    )
    ForbiddenCategory: ForbiddenCategoryEnum = Query(
        ForbiddenCategoryEnum.Other, alias="ForbiddenCategory"
    )
    Word: str = None
    Description: str = None
    AddDate: str = None
    ForbiddenNumber: str = None


@dataclass
class SearchForbiddenIn:
    ForbiddenID: str = Query(None)
    SysForbiddenID: str = None
    ForbiddenNumber: str = None
    Description: str = None
    ForbiddenType: ForbiddenTypeEnum = Query(
        ForbiddenTypeEnum.Other, alias="ForbiddenType"
    )
    ForbiddenCategory: ForbiddenCategoryEnum = Query(
        ForbiddenCategoryEnum.Other, alias="ForbiddenCategory"
    )
    Word: str = None
    AddDate: str = None
    size: int = Query(10, alias="PageSize")
    page: int = Query(1, alias="PageNumber")


@dataclass
class DelForbiddenIn:
    SysForbiddenID: str
