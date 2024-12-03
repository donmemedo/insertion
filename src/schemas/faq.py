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


class FAQTypeEnum(str, Enum):
    Lost = "Lost"
    Other = "Other"


class FAQCategoryEnum(str, Enum):
    Money = "Money"
    Hack = "Hack"


class SortOrder(IntEnum):
    ASCENDING = 1
    DESCENDING = -1


@dataclass
class AddFAQIn:
    FAQID: str
    FAQType: FAQTypeEnum = Query(
        FAQTypeEnum.Other, alias="FAQType"
    )
    FAQCategory: FAQCategoryEnum = Query(
        FAQCategoryEnum.Money, alias="FAQCategory"
    )
    Question: str = None
    Answer: str = None
    Description: str = None
    # AddDate: str = None


@dataclass
class ModifyFAQIn:
    SysFAQID: str
    FAQID: str
    FAQType: FAQTypeEnum = Query(
        FAQTypeEnum.Other, alias="FAQType"
    )
    FAQCategory: FAQCategoryEnum = Query(
        FAQCategoryEnum.Money, alias="FAQCategory"
    )
    Question: str = None
    Answer: str = None
    Description: str = None
    AddDate: str = None
    FAQNumber: str = None


@dataclass
class SearchFAQIn:
    FAQID: str = Query(None)
    SysFAQID: str = None
    FAQNumber: str = None
    Description: str = None
    FAQType: FAQTypeEnum = Query(
        FAQTypeEnum.Other, alias="FAQType"
    )
    FAQCategory: FAQCategoryEnum = Query(
        FAQCategoryEnum.Money, alias="FAQCategory"
    )
    Question: str = None
    Answer: str = None
    AddDate: str = None
    size: int = Query(10, alias="PageSize")
    page: int = Query(1, alias="PageNumber")


@dataclass
class DelFAQIn:
    SysFAQID: str
