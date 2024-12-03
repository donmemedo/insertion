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


class ProfessionalTypeEnum(str, Enum):
    Economy = "Economy"
    Other = "Other"


class ProfessionalCategoryEnum(str, Enum):
    Rule = "Rule"
    Other = "Other"


class SortOrder(IntEnum):
    ASCENDING = 1
    DESCENDING = -1


@dataclass
class AddProfessionalIn:
    ProfessionalID: str
    ProfessionalType: ProfessionalTypeEnum = Query(
        ProfessionalTypeEnum.Other, alias="ProfessionalType"
    )
    ProfessionalCategory: ProfessionalCategoryEnum = Query(
        ProfessionalCategoryEnum.Other, alias="ProfessionalCategory"
    )
    Word: str = None
    Description: str = None


@dataclass
class ModifyProfessionalIn:
    SysProfessionalID: str
    ProfessionalID: str
    ProfessionalType: ProfessionalTypeEnum = Query(
        ProfessionalTypeEnum.Other, alias="ProfessionalType"
    )
    ProfessionalCategory: ProfessionalCategoryEnum = Query(
        ProfessionalCategoryEnum.Other, alias="ProfessionalCategory"
    )
    Word: str = None
    Description: str = None
    AddDate: str = None
    ProfessionalNumber: str = None


@dataclass
class SearchProfessionalIn:
    ProfessionalID: str = Query(None)
    SysProfessionalID: str = None
    ProfessionalNumber: str = None
    Description: str = None
    ProfessionalType: ProfessionalTypeEnum = Query(
        ProfessionalTypeEnum.Other, alias="ProfessionalType"
    )
    ProfessionalCategory: ProfessionalCategoryEnum = Query(
        ProfessionalCategoryEnum.Other, alias="ProfessionalCategory"
    )
    Word: str = None
    AddDate: str = None
    size: int = Query(10, alias="PageSize")
    page: int = Query(1, alias="PageNumber")


@dataclass
class DelProfessionalIn:
    SysProfessionalID: str
