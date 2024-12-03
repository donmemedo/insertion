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
from src.schemas.tags import *
from src.utils.database import get_database
from src.utils.stages import *

tags_router = APIRouter(prefix="/tags")


@tags_router.post("/add", tags=["Tags"], response_model=None)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def add_tags(
        request: Request,
        atagsi: AddTagsIn,
        database: MongoClient = Depends(get_database),
        # role_perm: dict = Depends(get_role_permission),
):
    """_summary_

    Args:
        request (Request): _description_
        args (ModifyFactorIn, optional): _description_. Defaults to Depends(ModifyFactorIn).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    # user_id = role_perm["sub"]
    coll = database["Tags"]
    if atagsi.TagsID is None:
        raise RequestValidationError(TypeError, body={"code": "30003", "status": 412})
    filter = {"TagsID": atagsi.TagsID}
    update = {"$set": {}}
    update["$set"]["AddDate"] = jd.today().strftime("%Y-%m-%d")
    for key, value in vars(atagsi).items():
        if value is not None:
            update["$set"][key] = value
    # if atagsi.AddDate:
    #     try:
    #         StartDate = (
    #             jd(datetime.strptime(atagsi.AddDate, "%Y-%m-%d")).date().isoformat()
    #         )
    #     except:
    #         raise RequestValidationError(
    #             TypeError, body={"code": "30018", "status": 412}
    #         )

    update["$set"]["CreateDateTime"] = str(datetime.now())
    update["$set"]["SysTagsID"] = uuid.uuid1().hex
    update["$set"]["TagsType"] = TagsType[
        atagsi.TagsType.value
    ]
    update["$set"]["TagsCategory"] = TagsCategory[
        atagsi.TagsCategory.value
    ]
    update["$set"]["UpdateDateTime"] = str(datetime.now())
    update["$set"]["IsDeleted"] = False
    try:
        coll.insert_one(update["$set"])
    except:
        raise RequestValidationError(TypeError, body={"code": "30004", "status": 409})
    query_result = coll.find_one({"TagsID": atagsi.TagsID}, {"_id": False})

    resp = {
        "result": query_result,
        "timeGenerated": jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "error": {
            "message": "Null",
            "code": "Null",
        },
    }
    return JSONResponse(status_code=200, content=resp)


@tags_router.put(
    "/modify",
    tags=["Tags"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def modify_tags(
        request: Request,
        atagsi: ModifyTagsIn,
        database: MongoClient = Depends(get_database),
        # role_perm: dict = Depends(get_role_permission),
):
    """_summary_

    Args:
        request (Request): _description_
        args (ModifyFactorIn, optional): _description_. Defaults to Depends(ModifyFactorIn).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    # user_id = role_perm["sub"]
    coll = database["Tags"]
    if atagsi.TagsID is None:
        raise RequestValidationError(TypeError, body={"code": "30003", "status": 412})
    filter = {"TagsID": atagsi.TagsID}
    update = {"$set": {}}
    for key, value in vars(atagsi).items():
        if value is not None:
            update["$set"][key] = value
    if atagsi.AddDate:
        try:
            StartDate = (
                jd(datetime.strptime(atagsi.AddDate, "%Y-%m-%d")).date().isoformat()
            )
        except:
            raise RequestValidationError(
                TypeError, body={"code": "30004", "status": 412}
            )

    update["$set"]["UpdateDateTime"] = str(datetime.now())
    update["$set"]["IsDeleted"] = False
    coll.update_one(filter, update)
    query_result = coll.find_one({"TagsID": atagsi.TagsID}, {"_id": False})
    if not query_result:
        raise RequestValidationError(TypeError, body={"code": "30001", "status": 404})
    resp = {
        "result": query_result,
        "timeGenerated": jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "error": {
            "message": "Null",
            "code": "Null",
        },
    }
    return JSONResponse(status_code=200, content=resp)


@tags_router.get(
    "/search",
    tags=["Tags"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def search_tags(
        request: Request,
        args: SearchTagsIn = Depends(SearchTagsIn),
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
    coll = database["Tags"]
    upa = []

    if args.TagsID:
        upa.append({"TagsID": args.TagsID})
    if args.SysTagsID:
        upa.append({"SysTagsID": args.SysTagsID})
    if args.TagsNumber:
        upa.append({"TagsNumber": args.TagsNumber})
    if args.Description:
        upa.append({"Description": args.Description})
    if args.TagsType:
        upa.append({"TagsType": TagsType[args.TagsType.value]})
    if args.TagsCategory:
        upa.append(
            {"TagsCategory": TagsCategory[args.TagsCategory.value]}
        )
    if args.TagSubject:
        upa.append({"TagSubject": {"$regex": args.TagSubject}})
    if args.Tag:
        upa.append({"Tag": {"$regex": args.Tag}})
    # if args.AddDate:
    #     upa.append({"AddDate": {"$lte": args.AddDate}})
    if args.AddDate:
        upa.append({"AddDate": {"$gte": args.AddDate}})
    if upa:
        query = {"$and": upa}
    else:
        query = {}
    query_result = (
        coll.find(query, {"_id": False})
        .skip(args.size * (args.page - 1))
        .limit(args.size)
    )
    total_count = coll.count_documents(query)
    questions = dict(enumerate(query_result))
    results = []
    for i in range(len(questions)):
        results.append(questions[i])
    if not results:
        raise RequestValidationError(TypeError, body={"code": "30001", "status": 404})
    result = {}
    result["code"] = "Null"
    result["message"] = "Null"
    result["totalCount"] = total_count  # len(marketers)
    result["pagedData"] = results

    resp = {
        "result": result,
        "timeGenerated": jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "error": {
            "message": "Null",
            "code": "Null",
        },
    }
    return JSONResponse(status_code=200, content=resp)


@tags_router.delete(
    "/delete",
    tags=["Tags"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def delete_tags(
        request: Request,
        args: DelTagsIn = Depends(DelTagsIn),
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
    coll = database["Tags"]
    if args.SysTagsID:
        pass
    else:
        raise RequestValidationError(TypeError, body={"code": "30003", "status": 400})
    query_result = coll.find_one({"SysTagsID": args.SysTagsID}, {"_id": False})
    if not query_result:
        raise RequestValidationError(TypeError, body={"code": "30001", "status": 404})
    result = [f"مورد مربوط به تگ {query_result.get('TagSubject')} و {query_result.get('Tag')} پاک شد."]
    coll.delete_one({"SysTagsID": args.SysTagsID})
    resp = {
        "result": result,
        "timeGenerated": jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "error": {"message": "Null", "code": "Null"},
    }
    return JSONResponse(status_code=200, content=resp)


@tags_router.put(
    "/modify-status",
    tags=["Tags"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def modify_tags_status(
        request: Request,
        dmci: DelTagsIn,
        database: MongoClient = Depends(get_database),
        # role_perm: dict = Depends(get_role_permission),
):
    """_summary_

    Args:
        request (Request): _description_
        args (ModifyFactorIn, optional): _description_. Defaults to Depends(ModifyFactorIn).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    # user_id = role_perm["sub"]
    coll = database["Tags"]
    if dmci.SysTagsID is None:
        raise RequestValidationError(TypeError, body={"code": "30003", "status": 412})
    filter = {"SysTagsID": dmci.SysTagsID}
    query_result = coll.find_one({"SysTagsID": dmci.SysTagsID}, {"_id": False})
    status = query_result.get("IsDeleted")
    update = {"$set": {}}
    update["$set"]["IsDeleted"] = bool(status ^ 1)
    coll.update_one(filter, update)
    query_result = coll.find_one({"SysTagsID": dmci.SysTagsID}, {"_id": False})
    if not query_result:
        raise RequestValidationError(TypeError, body={"code": "30001", "status": 404})
    return ResponseListOut(
        result=query_result,
        timeGenerated=jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        error="",
    )


add_pagination(tags_router)
