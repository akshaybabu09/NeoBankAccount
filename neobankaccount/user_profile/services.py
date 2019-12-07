import random

from user_profile.constants import IFSC_CODES
from user_profile.models import UserProfile


def create_bank_account(user):
    user_ob = UserProfile.objects.get(user_id=user.user_id)
    # print(user_ob)
    user_ob.bank_account = user.mobile
    # user_ob.ifsc = 'abcd0001234'
    user_ob.save()

    print('Bank Account Created!!!!!!')


def display_account_details(user):
    account_details = UserProfile.objects.get(user_id=user.user_id)
    print('Bank Account Fetched!!!!')
    print(account_details.account_number)
    details = {
        'account_number': account_details.account_number,
        'ifsc': account_details.ifsc
    }
    print(details)
    return details


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
            'Mobile Number': user.mobile,
            'PAN Number': user.pan_detail,
            'Aadhaar Number': user.aadhaar_number,
            'Account Number': user.account_number,
            'IFSC Code': user.ifsc_code
        }, None
    return None, 'User Does not Exist!!!!'


def update_user_details(details):
    return 0
