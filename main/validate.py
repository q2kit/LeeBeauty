from .models import *

import re


def validate_address(province_id, district_id, commune_id):
    try:
        province = Province.objects.get(id=province_id)
        district = District.objects.get(id=district_id)
        commune = Commune.objects.get(id=commune_id)

        if province.id == district.province.id and district.id == commune.district.id:
            return True
        else:
            return False
    except:
        return False


def validate_email(email):
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)


def validate_phone(phone):
    return re.match(r"^[0-9]{10,11}$", phone)


def validate_password(password):
    return re.match(r"^[a-zA-Z0-9!@#$%^&*()_+]{8,}$", password)