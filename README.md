# NeoBankAccount

## Problem Statement

Using Django Rest Framework to create REST APIs to 
- Create a Neo Bank Account using Phone Number, PAN, Aadhaar.
- Fill in their personal information.
- Display the user details.

###### Note
The phone number acts as the account number.

## Stack Used
```
1. Python - 3.6.8
2. Django - 3.0
3. DRF - 3.10.3
4. PostgreSQL - 11.5
```

## Setup
```
git clone https://github.com/akshaybabu09/NeoBankAccount.git
cd neobankaccount
sudo apt-get update
sudo apt-get install python3.6
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Execution Flow
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Things Accomplished
1. User Account Creation
2. Fill in Personal Details
3. Access User Home with Token Authentication
4. Fetch Public Data of User with Phone Number (No Token Authentication)

## Things To Accomplish
Login & Logout Functionalities
