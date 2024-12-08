"""_summary_

Returns:
    _type_: _description_
"""
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
from khayyam import JalaliDatetime as jd
from pymongo import MongoClient

# from src.auth.authentication import get_role_permission
# from src.auth.authorization import authorize
from src.schemas.searches import *
from src.utils.config import settings
from src.utils.database import get_database
from src.utils.stages import *

search_router = APIRouter(prefix="/search", tags=["Search"])


@search_router.get(
    "/forbidden",
    tags=["Search"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def search_forbidden(
        request: Request,
        args: SearchIn = Depends(SearchIn),
        database: MongoClient = Depends(get_database),
        # role_perm: dict = Depends(get_role_permission),
):
    """_summary_

    Args:
        request (Request): _description_
        args (SearchFactorIn, optional): _description_. Defaults to Depends(SearchFactorIn).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    # user_id = role_perm["sub"]
    # permissions = [
    #     "Admin.All.All",
    # ]
    # allowed = check_permissions(role_perm["roles"], permissions)
    # if allowed:
    #     pass
    # else:
    #     raise HTTPException(status_code=403, detail="Not authorized.")
    coll = database[settings.FORBIDDEN_WORDS_COLLECTION]
    query_result = coll.find({}, {"_id": False})
    words = dict(enumerate(query_result))
    upa = []
    for word in words:
        upa.append(words[word]["Word"])

    if any([x in args.Context for x in upa]):
        keywords=[y for y in upa if y in args.Context]
    else:
        keywords=[""]
    result = {}
    result["code"] = "Null"
    result["message"] = "Null"
    result["totalCount"] = len(keywords)
    result["pagedData"] = keywords
    result["context"] = args.Context

    resp = {
        "result": result,
        "timeGenerated": jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "error": {
            "message": "Null",
            "code": "Null",
        },
    }
    return JSONResponse(status_code=200, content=resp)


@search_router.get(
    "/sensitive",
    tags=["Search"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def search_sensitive(
        request: Request,
        args: SearchIn = Depends(SearchIn),
        database: MongoClient = Depends(get_database),
        # role_perm: dict = Depends(get_role_permission),
):
    """_summary_

    Args:
        request (Request): _description_
        args (SearchFactorIn, optional): _description_. Defaults to Depends(SearchFactorIn).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    # user_id = role_perm["sub"]
    # permissions = [
    #     "Admin.All.All",
    # ]
    # allowed = check_permissions(role_perm["roles"], permissions)
    # if allowed:
    #     pass
    # else:
    #     raise HTTPException(status_code=403, detail="Not authorized.")
    coll = database[settings.SENSITIVE_WORDS_COLLECTION]
    query_result = coll.find({}, {"_id": False})
    words = dict(enumerate(query_result))
    upa = []
    for word in words:
        upa.append(words[word]["Word"])

    if any([x in args.Context for x in upa]):
        keywords=[y for y in upa if y in args.Context]
    else:
        keywords=[""]
    result = {}
    result["code"] = "Null"
    result["message"] = "Null"
    result["totalCount"] = len(keywords)
    result["pagedData"] = keywords
    result["context"] = args.Context

    resp = {
        "result": result,
        "timeGenerated": jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "error": {
            "message": "Null",
            "code": "Null",
        },
    }
    return JSONResponse(status_code=200, content=resp)


@search_router.get(
    "/professional",
    tags=["Search"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def search_professional(
        request: Request,
        args: SearchIn = Depends(SearchIn),
        database: MongoClient = Depends(get_database),
        # role_perm: dict = Depends(get_role_permission),
):
    """_summary_

    Args:
        request (Request): _description_
        args (SearchFactorIn, optional): _description_. Defaults to Depends(SearchFactorIn).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    # user_id = role_perm["sub"]
    # permissions = [
    #     "Admin.All.All",
    # ]
    # allowed = check_permissions(role_perm["roles"], permissions)
    # if allowed:
    #     pass
    # else:
    #     raise HTTPException(status_code=403, detail="Not authorized.")
    coll = database[settings.FORBIDDEN_WORDS_COLLECTION]
    query_result = coll.find({}, {"_id": False})
    words = dict(enumerate(query_result))
    upa = []
    for word in words:
        upa.append(words[word]["Word"])

    if any([x in args.Context for x in upa]):
        keywords=[y for y in upa if y in args.Context]
    else:
        keywords=[""]
    result = {}
    result["code"] = "Null"
    result["message"] = "Null"
    result["totalCount"] = len(keywords)
    result["pagedData"] = keywords
    result["context"] = args.Context

    resp = {
        "result": result,
        "timeGenerated": jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "error": {
            "message": "Null",
            "code": "Null",
        },
    }
    return JSONResponse(status_code=200, content=resp)




add_pagination(search_router)
