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


class TagsTypeEnum(str, Enum):
    Subjective = "Subjective"
    Objective = "Objective"
    Other = "Other"


class TagsCategoryEnum(str, Enum):
    CallReason = "CallReason"
    Other = "Other"


class SortOrder(IntEnum):
    ASCENDING = 1
    DESCENDING = -1


@dataclass
class AddTagsIn:
    TagsID: str
    TagsType: TagsTypeEnum = Query(
        TagsTypeEnum.Other, alias="TagsType"
    )
    TagsCategory: TagsCategoryEnum = Query(
        TagsCategoryEnum.Other, alias="TagsCategory"
    )
    TagSubject: str = None
    Tag: str = None
    Description: str = None
    # AddDate: str = None


@dataclass
class ModifyTagsIn:
    SysTagsID: str
    TagsID: str
    TagsType: TagsTypeEnum = Query(
        TagsTypeEnum.Other, alias="TagsType"
    )
    TagsCategory: TagsCategoryEnum = Query(
        TagsCategoryEnum.Other, alias="TagsCategory"
    )
    TagSubject: str = None
    Tag: str = None
    Description: str = None
    AddDate: str = None
    TagsNumber: str = None


@dataclass
class SearchTagsIn:
    TagsID: str = Query(None)
    SysTagsID: str = None
    TagsNumber: str = None
    Description: str = None
    TagsType: TagsTypeEnum = Query(
        TagsTypeEnum.Other, alias="TagsType"
    )
    TagsCategory: TagsCategoryEnum = Query(
        TagsCategoryEnum.Other, alias="TagsCategory"
    )
    TagSubject: str = None
    Tag: str = None
    AddDate: str = None
    size: int = Query(10, alias="PageSize")
    page: int = Query(1, alias="PageNumber")


@dataclass
class DelTagsIn:
    SysTagsID: str
