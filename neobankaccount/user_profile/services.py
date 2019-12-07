import random

from rest_framework.authtoken.models import Token

from user_profile.constants import *
from user_profile.models import UserProfile


def arrange_data(data):
    return {
        'mobile': data.get('mobile'),
        'password': data.get('passcode'),
        'aadhaar_number': data.get('aadhaar_number'),
        'pan_detail': data.get('pan_detail').upper(),
        'account_number': data.get('mobile'),
        'ifsc_code': random.choice(IFSC_CODES)
    }


def check_for_duplicate(data):
    obj = UserProfile.objects.filter(mobile=data.get('mobile'))
    if obj:
        return True, 'Phone Number Exists!!'
    obj = UserProfile.objects.filter(aadhaar_number=data.get('aadhaar_number'))
    if obj:
        return True, 'Aadhaar Number Exists!!'
    obj = UserProfile.objects.filter(pan_detail=data.get('pan_detail'))
    if obj:
        return True, 'PAN Number Exists!!'
    return False, None


def fetch_user_details_from_mobile(mobile):
    user = UserProfile.objects.get(mobile=mobile)
    if user:
        return {
            'Name': user.display_name,
            'Mobile Number': user.mobile,
            'Account Number': user.account_number,
            'IFSC Code': user.ifsc_code
        }, None
    return None, 'User Does not Exist!!!!'


def fetch_user_details(user):
    return {
        'Name': user.display_name,
        'Mobile Number': user.mobile,
        'Email': user.email,
        'Address': user.address,
        'Pincode': user.pincode,
        'PAN Number': user.pan_detail,
        'Aadhaar Number': user.aadhaar_number,
        'Account Number': user.account_number,
        'IFSC Code': user.ifsc_code
        }, None


def update_user_details(user, user_data):
    user.display_name = user_data.get('display_name', None).upper()
    user.gender = user_data.get('gender', None)
    user.address = user_data.get('address', None)
    user.pincode = user_data.get('pincode', None)
    user.email = user_data.get('email', None)
    user.save()

    return True


def fetch_token_for_user(user, register=False):
    token, created = Token.objects.get_or_create(user=user)
    if register:
        return {
            'token': token.key,
            'msg': ACCOUNT_CREATED_MSG
        }
    return {
        'token': token.key,
        'message': LOGIN_MSG
    }
