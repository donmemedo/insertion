errors_mapping = {
    "30001": "موردی در دیتابیس یافت نشد.",
    "30002": "موردی با متغیرهای داده شده یافت نشد.",
    "30003": "خروجی برای متغیرهای داده شده نداریم.",
    "30004": "ورودی ها را دوباره چک کنید.",
}


def get_error(type: str, code: str):
    if type == "TypeError":
        return {"code": code, "message": errors_mapping[code]}
    if type == "json_invalid":
        return {"code": 400, "message": code}
    if type == "missing":
        return {"code": 412, "message": code}
    if type == "enum":
        return {"code": 412, "message": code}