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
from src.schemas.forbidden import *
from src.utils.database import get_database
from src.utils.stages import *

forbidden_router = APIRouter(prefix="/forbidden")


@forbidden_router.post("/add", tags=["Forbidden"], response_model=None)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def add_forbidden(
        request: Request,
        aforbiddeni: AddForbiddenIn,
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
    coll = database["Forbidden"]
    if aforbiddeni.ForbiddenID is None:
        raise RequestValidationError(TypeError, body={"code": "30003", "status": 412})
    filter = {"ForbiddenID": aforbiddeni.ForbiddenID}
    update = {"$set": {}}
    update["$set"]["AddDate"] = jd.today().strftime("%Y-%m-%d")
    for key, value in vars(aforbiddeni).items():
        if value is not None:
            update["$set"][key] = value
    # if aforbiddeni.AddDate:
    #     try:
    #         StartDate = (
    #             jd(datetime.strptime(aforbiddeni.AddDate, "%Y-%m-%d")).date().isoformat()
    #         )
    #     except:
    #         raise RequestValidationError(
    #             TypeError, body={"code": "30018", "status": 412}
    #         )

    update["$set"]["CreateDateTime"] = str(datetime.now())
    update["$set"]["SysForbiddenID"] = uuid.uuid1().hex
    update["$set"]["ForbiddenType"] = ForbiddenType[
        aforbiddeni.ForbiddenType.value
    ]
    update["$set"]["ForbiddenCategory"] = ForbiddenCategory[
        aforbiddeni.ForbiddenCategory.value
    ]
    update["$set"]["UpdateDateTime"] = str(datetime.now())
    update["$set"]["IsDeleted"] = False

    try:
        coll.insert_one(update["$set"])
    except:
        raise RequestValidationError(TypeError, body={"code": "30004", "status": 409})
    query_result = coll.find_one({"ForbiddenID": aforbiddeni.ForbiddenID}, {"_id": False})

    resp = {
        "result": query_result,
        "timeGenerated": jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "error": {
            "message": "Null",
            "code": "Null",
        },
    }
    return JSONResponse(status_code=200, content=resp)


@forbidden_router.put(
    "/modify",
    tags=["Forbidden"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def modify_forbidden(
        request: Request,
        aforbiddeni: ModifyForbiddenIn,
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
    coll = database["Forbidden"]
    if aforbiddeni.ForbiddenID is None:
        raise RequestValidationError(TypeError, body={"code": "30003", "status": 412})
    filter = {"ForbiddenID": aforbiddeni.ForbiddenID}
    update = {"$set": {}}
    for key, value in vars(aforbiddeni).items():
        if value is not None:
            update["$set"][key] = value
    if aforbiddeni.AddDate:
        try:
            StartDate = (
                jd(datetime.strptime(aforbiddeni.AddDate, "%Y-%m-%d")).date().isoformat()
            )
        except:
            raise RequestValidationError(
                TypeError, body={"code": "30004", "status": 412}
            )

    update["$set"]["UpdateDateTime"] = str(datetime.now())
    update["$set"]["IsDeleted"] = False
    coll.update_one(filter, update)
    query_result = coll.find_one({"ForbiddenID": aforbiddeni.ForbiddenID}, {"_id": False})
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


@forbidden_router.get(
    "/search",
    tags=["Forbidden"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def search_forbidden(
        request: Request,
        args: SearchForbiddenIn = Depends(SearchForbiddenIn),
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
    coll = database["Forbidden"]
    upa = []

    if args.ForbiddenID:
        upa.append({"ForbiddenID": args.ForbiddenID})
    if args.SysForbiddenID:
        upa.append({"SysForbiddenID": args.SysForbiddenID})
    if args.ForbiddenNumber:
        upa.append({"ForbiddenNumber": args.ForbiddenNumber})
    if args.Description:
        upa.append({"Description": args.Description})
    if args.ForbiddenType:
        upa.append({"ForbiddenType": ForbiddenType[args.ForbiddenType.value]})
    if args.ForbiddenCategory:
        upa.append(
            {"ForbiddenCategory": ForbiddenCategory[args.ForbiddenCategory.value]}
        )
    if args.Word:
        upa.append({"Word": {"$regex": args.Word}})
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


@forbidden_router.delete(
    "/delete",
    tags=["Forbidden"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def delete_forbidden(
        request: Request,
        args: DelForbiddenIn = Depends(DelForbiddenIn),
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
    coll = database["Forbidden"]
    if args.SysForbiddenID:
        pass
    else:
        raise RequestValidationError(TypeError, body={"code": "30003", "status": 400})
    query_result = coll.find_one({"SysForbiddenID": args.SysForbiddenID}, {"_id": False})
    if not query_result:
        raise RequestValidationError(TypeError, body={"code": "30001", "status": 404})
    result = [f"مورد مربوط به کلمه {query_result.get('Word')} پاک شد."]
    coll.delete_one({"SysForbiddenID": args.SysForbiddenID})
    resp = {
        "result": result,
        "timeGenerated": jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "error": {"message": "Null", "code": "Null"},
    }
    return JSONResponse(status_code=200, content=resp)


@forbidden_router.put(
    "/modify-status",
    tags=["Forbidden"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def modify_forbidden_status(
        request: Request,
        dmci: DelForbiddenIn,
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
    coll = database["Forbidden"]
    if dmci.SysForbiddenID is None:
        raise RequestValidationError(TypeError, body={"code": "30003", "status": 412})
    filter = {"SysForbiddenID": dmci.SysForbiddenID}
    query_result = coll.find_one({"SysForbiddenID": dmci.SysForbiddenID}, {"_id": False})
    status = query_result.get("IsDeleted")
    update = {"$set": {}}
    update["$set"]["IsDeleted"] = bool(status ^ 1)
    coll.update_one(filter, update)
    query_result = coll.find_one({"SysForbiddenID": dmci.SysForbiddenID}, {"_id": False})
    if not query_result:
        raise RequestValidationError(TypeError, body={"code": "30001", "status": 404})
    return ResponseListOut(
        result=query_result,
        timeGenerated=jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        error="",
    )


add_pagination(forbidden_router)
