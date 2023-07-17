from django.conf import settings

from rest_framework.response import Response
from rest_framework import  status
from rest_framework.views import APIView

from payments.tasks import perform_stk_push

class STKPushAPIView(APIView):
    """
    API view for initiating STK push transactions.
    
    Example:
    
    {
        "phone_number": "1234567890",
        "amount": 1,
        "account_reference": "ABC123",
        "transaction_desc": "Example transaction"
    }
    """
    def post(self, request):
        """
        Handles the POST request to initiate an STK push transaction.

        Required parameters in request.data:
        - phone_number: Phone number of the recipient.
        - amount: Amount to be transacted.
        - account_reference: Account reference for the transaction.
        - transaction_desc: Description of the transaction.
        - callback_url: URL to receive callback notifications.

        Returns:
        - If the transaction is successful, returns the response data with a 200 OK status.
        - If an error occurs, returns the error message with a 400 Bad Request status.
        """
        phone_number = request.data.get('phone_number')
        amount = request.data.get('amount')
        account_reference = request.data.get('account_reference')
        transaction_desc = request.data.get('transaction_desc')
        callback_url = getattr(settings, 'MPESA_CALLBACK_URL', None)

        if not all([phone_number, amount, account_reference, transaction_desc, callback_url]):
            return Response("Missing required parameters", status=status.HTTP_400_BAD_REQUEST)

        perform_stk_push.delay(phone_number, amount, account_reference, transaction_desc, callback_url)

        return Response("STK push initiated", status=status.HTTP_200_OK)


class MPESACallBackAPIView(APIView):
    """
    API view for handling STK push callback notifications.
    """
    def post(self, request):
        """
        Handles the POST request for STK push callback notifications.

        Returns the received data with a 200 OK status.
        """
        data = request.data
        return Response(data, status=status.HTTP_200_OK)
