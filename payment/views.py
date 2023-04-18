from django.shortcuts import render
from django.conf import settings
import requests
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import timedelta , datetime

#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/verify/'

@login_required
def send_request(request):
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Description": description,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    try:
        response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return HttpResponse({'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']})
            else:
                return HttpResponse({'status': False, 'code': str(response['Status'])})
        return response
    
    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return HttpResponse ({'status': False, 'code': 'connection error'})


@login_required
def verify(authority,request):
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            user = request.user
            user.special_user =  datetime.now() + timedelta(days=30)

            return HttpResponse({'status': True, 'RefID': response['RefID']})
        else:
            return HttpResponse({'status': False, 'code': str(response['Status'])})
    return response
