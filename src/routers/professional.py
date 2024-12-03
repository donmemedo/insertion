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
from src.schemas.professional import *
from src.utils.database import get_database
from src.utils.stages import *

professional_router = APIRouter(prefix="/professional")


@professional_router.post("/add", tags=["Professional"], response_model=None)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def add_professional(
        request: Request,
        aprofessionali: AddProfessionalIn,
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
    coll = database["Professional"]
    if aprofessionali.ProfessionalID is None:
        raise RequestValidationError(TypeError, body={"code": "30003", "status": 412})
    filter = {"ProfessionalID": aprofessionali.ProfessionalID}
    update = {"$set": {}}
    update["$set"]["AddDate"] = jd.today().strftime("%Y-%m-%d")
    for key, value in vars(aprofessionali).items():
        if value is not None:
            update["$set"][key] = value
    # if aprofessionali.AddDate:
    #     try:
    #         StartDate = (
    #             jd(datetime.strptime(aprofessionali.AddDate, "%Y-%m-%d")).date().isoformat()
    #         )
    #     except:
    #         raise RequestValidationError(
    #             TypeError, body={"code": "30018", "status": 412}
    #         )

    update["$set"]["CreateDateTime"] = str(datetime.now())
    update["$set"]["SysProfessionalID"] = uuid.uuid1().hex
    update["$set"]["ProfessionalType"] = ProfessionalType[
        aprofessionali.ProfessionalType.value
    ]
    update["$set"]["ProfessionalCategory"] = ProfessionalCategory[
        aprofessionali.ProfessionalCategory.value
    ]
    update["$set"]["UpdateDateTime"] = str(datetime.now())
    update["$set"]["IsDeleted"] = False

    try:
        coll.insert_one(update["$set"])
    except:
        raise RequestValidationError(TypeError, body={"code": "30004", "status": 409})
    query_result = coll.find_one({"ProfessionalID": aprofessionali.ProfessionalID}, {"_id": False})

    resp = {
        "result": query_result,
        "timeGenerated": jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "error": {
            "message": "Null",
            "code": "Null",
        },
    }
    return JSONResponse(status_code=200, content=resp)


@professional_router.put(
    "/modify",
    tags=["Professional"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def modify_professional(
        request: Request,
        aprofessionali: ModifyProfessionalIn,
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
    coll = database["Professional"]
    if aprofessionali.ProfessionalID is None:
        raise RequestValidationError(TypeError, body={"code": "30003", "status": 412})
    filter = {"ProfessionalID": aprofessionali.ProfessionalID}
    update = {"$set": {}}
    for key, value in vars(aprofessionali).items():
        if value is not None:
            update["$set"][key] = value
    if aprofessionali.AddDate:
        try:
            StartDate = (
                jd(datetime.strptime(aprofessionali.AddDate, "%Y-%m-%d")).date().isoformat()
            )
        except:
            raise RequestValidationError(
                TypeError, body={"code": "30004", "status": 412}
            )

    update["$set"]["UpdateDateTime"] = str(datetime.now())
    update["$set"]["IsDeleted"] = False
    coll.update_one(filter, update)
    query_result = coll.find_one({"ProfessionalID": aprofessionali.ProfessionalID}, {"_id": False})
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


@professional_router.get(
    "/search",
    tags=["Professional"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def search_professional(
        request: Request,
        args: SearchProfessionalIn = Depends(SearchProfessionalIn),
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
    coll = database["Professional"]
    upa = []

    if args.ProfessionalID:
        upa.append({"ProfessionalID": args.ProfessionalID})
    if args.SysProfessionalID:
        upa.append({"SysProfessionalID": args.SysProfessionalID})
    if args.ProfessionalNumber:
        upa.append({"ProfessionalNumber": args.ProfessionalNumber})
    if args.Description:
        upa.append({"Description": args.Description})
    if args.ProfessionalType:
        upa.append({"ProfessionalType": ProfessionalType[args.ProfessionalType.value]})
    if args.ProfessionalCategory:
        upa.append(
            {"ProfessionalCategory": ProfessionalCategory[args.ProfessionalCategory.value]}
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


@professional_router.delete(
    "/delete",
    tags=["Professional"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def delete_professional(
        request: Request,
        args: DelProfessionalIn = Depends(DelProfessionalIn),
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
    coll = database["Professional"]
    if args.SysProfessionalID:
        pass
    else:
        raise RequestValidationError(TypeError, body={"code": "30003", "status": 400})
    query_result = coll.find_one({"SysProfessionalID": args.SysProfessionalID}, {"_id": False})
    if not query_result:
        raise RequestValidationError(TypeError, body={"code": "30001", "status": 404})
    result = [f"مورد مربوط به کلمه {query_result.get('Word')} پاک شد."]
    coll.delete_one({"SysProfessionalID": args.SysProfessionalID})
    resp = {
        "result": result,
        "timeGenerated": jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "error": {"message": "Null", "code": "Null"},
    }
    return JSONResponse(status_code=200, content=resp)


@professional_router.put(
    "/modify-status",
    tags=["Professional"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def modify_professional_status(
        request: Request,
        dmci: DelProfessionalIn,
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
    coll = database["Professional"]
    if dmci.SysProfessionalID is None:
        raise RequestValidationError(TypeError, body={"code": "30003", "status": 412})
    filter = {"SysProfessionalID": dmci.SysProfessionalID}
    query_result = coll.find_one({"SysProfessionalID": dmci.SysProfessionalID}, {"_id": False})
    status = query_result.get("IsDeleted")
    update = {"$set": {}}
    update["$set"]["IsDeleted"] = bool(status ^ 1)
    coll.update_one(filter, update)
    query_result = coll.find_one({"SysProfessionalID": dmci.SysProfessionalID}, {"_id": False})
    if not query_result:
        raise RequestValidationError(TypeError, body={"code": "30001", "status": 404})
    return ResponseListOut(
        result=query_result,
        timeGenerated=jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        error="",
    )


add_pagination(professional_router)
