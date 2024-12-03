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
from src.schemas.faq import *
from src.utils.database import get_database
from src.utils.stages import *

faq_router = APIRouter(prefix="/faq")


@faq_router.post("/add", tags=["FAQ"], response_model=None)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def add_faq(
        request: Request,
        afaqi: AddFAQIn,
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
    coll = database["FAQ"]
    if afaqi.FAQID is None:
        raise RequestValidationError(TypeError, body={"code": "30003", "status": 412})
    filter = {"FAQID": afaqi.FAQID}
    update = {"$set": {}}
    update["$set"]["AddDate"] = jd.today().strftime("%Y-%m-%d")
    for key, value in vars(afaqi).items():
        if value is not None:
            update["$set"][key] = value
    # if afaqi.AddDate:
    #     try:
    #         StartDate = (
    #             jd(datetime.strptime(afaqi.AddDate, "%Y-%m-%d")).date().isoformat()
    #         )
    #     except:
    #         raise RequestValidationError(
    #             TypeError, body={"code": "30018", "status": 412}
    #         )

    update["$set"]["CreateDateTime"] = str(datetime.now())
    update["$set"]["SysFAQID"] = uuid.uuid1().hex
    update["$set"]["FAQType"] = FAQType[
        afaqi.FAQType.value
    ]
    update["$set"]["FAQCategory"] = FAQCategory[
        afaqi.FAQCategory.value
    ]
    update["$set"]["UpdateDateTime"] = str(datetime.now())
    update["$set"]["IsDeleted"] = False

    try:
        coll.insert_one(update["$set"])
    except:
        raise RequestValidationError(TypeError, body={"code": "30007", "status": 409})
    query_result = coll.find_one({"FAQID": afaqi.FAQID}, {"_id": False})

    resp = {
        "result": query_result,
        "timeGenerated": jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "error": {
            "message": "Null",
            "code": "Null",
        },
    }
    return JSONResponse(status_code=200, content=resp)


@faq_router.put(
    "/modify",
    tags=["FAQ"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def modify_faq(
        request: Request,
        afaqi: ModifyFAQIn,
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
    coll = database["FAQ"]
    if afaqi.FAQID is None:
        raise RequestValidationError(TypeError, body={"code": "30003", "status": 412})
    filter = {"FAQID": afaqi.FAQID}
    update = {"$set": {}}
    for key, value in vars(afaqi).items():
        if value is not None:
            update["$set"][key] = value
    if afaqi.AddDate:
        try:
            StartDate = (
                jd(datetime.strptime(afaqi.AddDate, "%Y-%m-%d")).date().isoformat()
            )
        except:
            raise RequestValidationError(
                TypeError, body={"code": "30018", "status": 412}
            )

    update["$set"]["UpdateDateTime"] = str(datetime.now())
    update["$set"]["IsDeleted"] = False
    coll.update_one(filter, update)
    query_result = coll.find_one({"FAQID": afaqi.FAQID}, {"_id": False})
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


@faq_router.get(
    "/search",
    tags=["FAQ"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def search_faq(
        request: Request,
        args: SearchFAQIn = Depends(SearchFAQIn),
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
    coll = database["FAQ"]
    upa = []

    if args.FAQID:
        upa.append({"FAQID": args.FAQID})
    if args.SysFAQID:
        upa.append({"SysFAQID": args.SysFAQID})
    if args.FAQNumber:
        upa.append({"FAQNumber": args.FAQNumber})
    if args.Description:
        upa.append({"Description": args.Description})
    if args.FAQType:
        upa.append({"FAQType": FAQType[args.FAQType.value]})
    if args.FAQCategory:
        upa.append(
            {"FAQCategory": FAQCategory[args.FAQCategory.value]}
        )
    if args.Question:
        upa.append({"Question": {"$regex": args.Question}})
    if args.Answer:
        upa.append({"Answer": {"$regex": args.Answer}})
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


@faq_router.delete(
    "/delete",
    tags=["FAQ"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def delete_faq(
        request: Request,
        args: DelFAQIn = Depends(DelFAQIn),
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
    coll = database["FAQ"]
    if args.SysFAQID:
        pass
    else:
        raise RequestValidationError(TypeError, body={"code": "30003", "status": 400})
    query_result = coll.find_one({"SysFAQID": args.SysFAQID}, {"_id": False})
    if not query_result:
        raise RequestValidationError(TypeError, body={"code": "30001", "status": 404})
    result = [f"مورد مربوط به سوال {query_result.get('Question')} پاک شد."]
    coll.delete_one({"SysFAQID": args.SysFAQID})
    resp = {
        "result": result,
        "timeGenerated": jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "error": {"message": "Null", "code": "Null"},
    }
    return JSONResponse(status_code=200, content=resp)


@faq_router.put(
    "/modify-status",
    tags=["FAQ"],
)
# @authorize(
#     [
#         "PERMISSIONS",
#         "Admin.All.All",
#     ]
# )
async def modify_faq_status(
        request: Request,
        dmci: DelFAQIn,
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
    coll = database["FAQ"]
    if dmci.SysFAQID is None:
        raise RequestValidationError(TypeError, body={"code": "30003", "status": 412})
    filter = {"ContractID": dmci.SysFAQID}
    query_result = coll.find_one({"SysFAQID": dmci.SysFAQID}, {"_id": False})
    status = query_result.get("IsDeleted")
    update = {"$set": {}}
    update["$set"]["IsDeleted"] = bool(status ^ 1)
    coll.update_one(filter, update)
    query_result = coll.find_one({"SysFAQID": dmci.SysFAQID}, {"_id": False})
    if not query_result:
        raise RequestValidationError(TypeError, body={"code": "30001", "status": 404})
    return ResponseListOut(
        result=query_result,
        timeGenerated=jd.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        error="",
    )


add_pagination(faq_router)
