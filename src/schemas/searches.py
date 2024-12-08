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


class SortOrder(IntEnum):
    ASCENDING = 1
    DESCENDING = -1


@dataclass
class SearchIn:
    Context: str = None
    size: int = Query(10, alias="PageSize")
    page: int = Query(1, alias="PageNumber")
