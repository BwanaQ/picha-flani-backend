from celery import shared_task
from django_daraja.mpesa.core import MpesaClient

@shared_task
def perform_stk_push(phone_number, amount, account_reference, transaction_desc, callback_url):
    mpesa_client = MpesaClient()
    response = mpesa_client.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return response
